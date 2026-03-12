"""
MoodBeats — Prolog Bridge
prolog_bridge.py

Manages the SWI-Prolog subprocess and provides a clean Python API
for querying the expert system knowledge base.

The bridge uses pyswip to load moodbeats.pl and execute queries,
returning structured Python dicts instead of raw Prolog output.
"""

import os
import sys
from pathlib import Path
from pyswip import Prolog, Atom, Functor, Variable

# ── Paths ─────────────────────────────────────────────────────
_HERE = Path(__file__).parent
KB_PATH = (_HERE / ".." / "knowledge_base" / "moodbeats.pl").resolve()

# ── Valid atoms ───────────────────────────────────────────────
VALID_MOODS = [
    "happy", "energetic", "motivated", "confident",
    "angry", "anxious", "stressed",
    "sad", "melancholic", "tired", "bored",
    "calm", "romantic", "nostalgic", "focused",
]

VALID_ACTIVITIES = [
    "studying", "deep_work", "light_work",
    "working_out", "commuting", "chores",
    "socializing", "romance", "grieving_venting",
    "relaxing", "sleeping", "meditating",
]

VALID_COGNITIVE_LOADS = ["high", "moderate", "low"]


# ── Singleton Prolog engine ───────────────────────────────────
_prolog: Prolog | None = None


def _get_prolog() -> Prolog:
    """Return (and lazily initialise) the singleton Prolog engine."""
    global _prolog
    if _prolog is None:
        _prolog = Prolog()
        kb_str = str(KB_PATH)
        try:
            _prolog.consult(kb_str)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load Prolog knowledge base at '{kb_str}': {exc}"
            ) from exc
    return _prolog


def reload_knowledge_base() -> None:
    """Force a fresh reload of the knowledge base (e.g. after songs_kb rebuild)."""
    global _prolog
    _prolog = None
    _get_prolog()


# ── Query helpers ─────────────────────────────────────────────

def _atom(value) -> str:
    """Convert a pyswip Atom to str, or return as-is if already str."""
    if isinstance(value, Atom):
        return str(value)
    return str(value)


def _safe_float(val) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _safe_int(val) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0


# ── Public API ────────────────────────────────────────────────

def recommend(
    mood: str,
    activity: str,
    cognitive_load: str,
    playlist_size: int = 10,
) -> dict:
    """
    Run the expert system and return a structured recommendation dict.

    Parameters
    ----------
    mood           : atom from VALID_MOODS
    activity       : atom from VALID_ACTIVITIES
    cognitive_load : atom from VALID_COGNITIVE_LOADS
    playlist_size  : max number of tracks to return

    Returns
    -------
    {
        "mood": str,
        "activity": str,
        "cognitive_load": str,
        "playlist": [
            {
                "id": str,
                "title": str,
                "artist": str,
                "bpm": int,
                "energy": float,
                "instrumentalness": float,
                "valence": float,
                "tone": str,
                "lyric_complexity": str,
            }, ...
        ],
        "explanations": [
            {
                "id": str,
                "title": str,
                "artist": str,
                "valence_in_range": bool,
                "energy_in_range": bool,
                "tone_compatible": bool,
                "bpm_in_range": bool,
                "lyric_compatible": bool,
                "mood_valence_range": [float, float],
                "mood_energy_range": [float, float],
                "mood_tones": [str],
                "activity_bpm_range": [int, int],
            }, ...
        ],
        "fallback": bool,
        "fallback_message": str | None,
    }
    """
    if mood not in VALID_MOODS:
        raise ValueError(f"Unknown mood '{mood}'. Valid moods: {VALID_MOODS}")
    if activity not in VALID_ACTIVITIES:
        raise ValueError(f"Unknown activity '{activity}'. Valid activities: {VALID_ACTIVITIES}")
    if cognitive_load not in VALID_COGNITIVE_LOADS:
        raise ValueError(
            f"Unknown cognitive_load '{cognitive_load}'. "
            f"Valid values: {VALID_COGNITIVE_LOADS}"
        )

    prolog = _get_prolog()

    # Step 1: get the playlist of track IDs via safe_recommend/5
    playlist_ids = _get_playlist_ids(prolog, mood, activity, cognitive_load, playlist_size)

    # Step 2: detect fallback
    fallback, fallback_msg = _detect_fallback(
        prolog, mood, activity, cognitive_load, playlist_size, playlist_ids
    )

    # Step 3: fetch full song info for each ID
    playlist = []
    for sid in playlist_ids:
        info = _get_song_info(prolog, sid)
        if info:
            playlist.append(info)

    # Step 4: build explanations
    explanations = []
    for sid in playlist_ids:
        exp = _build_explanation(prolog, sid, mood, activity, cognitive_load)
        if exp:
            explanations.append(exp)

    return {
        "mood": mood,
        "activity": activity,
        "cognitive_load": cognitive_load,
        "playlist": playlist,
        "explanations": explanations,
        "fallback": fallback,
        "fallback_message": fallback_msg if fallback else None,
    }


def _get_playlist_ids(prolog, mood, activity, cognitive_load, size) -> list[str]:
    """Query safe_recommend/5 and return list of track ID strings."""
    query = (
        f"safe_recommend({mood}, {activity}, {cognitive_load}, {size}, Playlist)"
    )
    try:
        results = list(prolog.query(query))
        if results:
            raw_list = results[0]["Playlist"]
            return [_atom(item) for item in raw_list]
    except Exception:
        pass
    return []


def _detect_fallback(prolog, mood, activity, cognitive_load, size, actual_ids) -> tuple[bool, str | None]:
    """Determine whether the fallback path was taken."""
    if not actual_ids:
        return False, None

    # Try the strict recommend — if it returns empty, fallback was used
    strict_query = (
        f"recommend({mood}, {activity}, {cognitive_load}, 0, 300, {size}, Playlist)"
    )
    try:
        results = list(prolog.query(strict_query))
        if results:
            strict = results[0]["Playlist"]
            if strict:
                return False, None
    except Exception:
        pass

    return True, "No perfect match found; playlist generated using mood profile only."


def _get_song_info(prolog, song_id: str) -> dict | None:
    """Fetch full song attributes for a given track ID."""
    query = (
        f"song('{song_id}', Title, Artist, BPM, Energy, Instr, Valence, Tone, Complexity)"
    )
    try:
        results = list(prolog.query(query))
        if results:
            r = results[0]
            return {
                "id": song_id,
                "title": _atom(r["Title"]),
                "artist": _atom(r["Artist"]),
                "bpm": _safe_int(r["BPM"]),
                "energy": _safe_float(r["Energy"]),
                "instrumentalness": _safe_float(r["Instr"]),
                "valence": _safe_float(r["Valence"]),
                "tone": _atom(r["Tone"]),
                "lyric_complexity": _atom(r["Complexity"]),
            }
    except Exception:
        pass
    return None


def _build_explanation(prolog, song_id: str, mood, activity, cognitive_load) -> dict | None:
    """Build an explanation dict for why a track was selected."""
    song_info = _get_song_info(prolog, song_id)
    if not song_info:
        return None

    # Fetch mood profile
    mood_q = (
        f"mood_profile({mood}, ValLow, ValHigh, EnLow, EnHigh, Tones)"
    )
    mood_data = {}
    try:
        mp = list(prolog.query(mood_q))
        if mp:
            r = mp[0]
            mood_data = {
                "valence_range": [_safe_float(r["ValLow"]), _safe_float(r["ValHigh"])],
                "energy_range": [_safe_float(r["EnLow"]), _safe_float(r["EnHigh"])],
                "tones": [_atom(t) for t in r["Tones"]],
            }
    except Exception:
        pass

    # Fetch activity profile
    act_q = f"activity_profile({activity}, MinBPM, MaxBPM)"
    act_data = {}
    try:
        ap = list(prolog.query(act_q))
        if ap:
            r = ap[0]
            act_data = {
                "bpm_range": [_safe_int(r["MinBPM"]), _safe_int(r["MaxBPM"])],
            }
    except Exception:
        pass

    # Check compatibility predicates
    vl, vh = mood_data.get("valence_range", [0, 1])
    el, eh = mood_data.get("energy_range", [0, 1])
    bmin, bmax = act_data.get("bpm_range", [0, 300])
    tones = mood_data.get("tones", [])

    val = song_info["valence"]
    eng = song_info["energy"]
    bpm = song_info["bpm"]
    tone = song_info["tone"]
    lc = song_info["lyric_complexity"]

    val_in = vl <= val <= vh
    eng_in = el <= eng <= eh
    bpm_in = bmin <= bpm <= bmax
    tone_ok_q = f"tone_compatible({tone}, {tones})"
    tone_ok = False
    try:
        tone_ok = bool(list(prolog.query(tone_ok_q)))
    except Exception:
        tone_ok = tone in tones

    lyric_ok_q = f"lyric_compatible({lc}, {cognitive_load}, {activity})"
    lyric_ok = False
    try:
        lyric_ok = bool(list(prolog.query(lyric_ok_q)))
    except Exception:
        pass

    return {
        "id": song_id,
        "title": song_info["title"],
        "artist": song_info["artist"],
        "valence": val,
        "energy": eng,
        "bpm": bpm,
        "tone": tone,
        "lyric_complexity": lc,
        "mood_valence_range": [vl, vh],
        "mood_energy_range": [el, eh],
        "mood_tones": tones,
        "activity_bpm_range": [bmin, bmax],
        "valence_in_range": val_in,
        "energy_in_range": eng_in,
        "tone_compatible": tone_ok,
        "bpm_in_range": bpm_in,
        "lyric_compatible": lyric_ok,
    }


def get_moods() -> list[str]:
    """Return all available mood atoms."""
    return list(VALID_MOODS)


def get_activities() -> list[str]:
    """Return all available activity atoms."""
    return list(VALID_ACTIVITIES)


def get_cognitive_loads() -> list[str]:
    """Return valid cognitive load atoms."""
    return list(VALID_COGNITIVE_LOADS)


def get_all_songs() -> list[dict]:
    """Return all songs from the knowledge base."""
    prolog = _get_prolog()
    query = "song(ID, Title, Artist, BPM, Energy, Instr, Valence, Tone, Complexity)"
    songs = []
    try:
        for r in prolog.query(query):
            songs.append({
                "id": _atom(r["ID"]),
                "title": _atom(r["Title"]),
                "artist": _atom(r["Artist"]),
                "bpm": _safe_int(r["BPM"]),
                "energy": _safe_float(r["Energy"]),
                "instrumentalness": _safe_float(r["Instr"]),
                "valence": _safe_float(r["Valence"]),
                "tone": _atom(r["Tone"]),
                "lyric_complexity": _atom(r["Complexity"]),
            })
    except Exception:
        pass
    return songs
