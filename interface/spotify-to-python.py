# ============================================================
# MoodBeats — Spotify to Prolog Bridge
# spotify_to_prolog.py
#
# Fetches tracks and audio features from Spotify and writes
# them as Prolog facts to songs_kb.pl.
#
# LyricTone is determined by a three-tier resolution system:
#   Tier 1 — Valence + Energy quadrant mapping (automatic)
#   Tier 2 — Spotify audio feature refinement (automatic)
#   Tier 3 — Manual override table (KE-editable, see below)
#
# Setup:
#   1. pip install spotipy
#   2. Fill in CLIENT_ID and CLIENT_SECRET below
#   3. Replace playlist IDs in MOOD_PLAYLISTS with real IDs
#      sourced from your domain expert
#   4. Run: python spotify_to_prolog.py
# ============================================================

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# ── Credentials ──────────────────────────────────────────────
# Register an app at https://developer.spotify.com to get these
CLIENT_ID     = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))


# ── Mood-to-Playlist Seed Map ────────────────────────────────
# Maps each of the 15 mood atoms to one or more Spotify
# playlist IDs. Replace placeholder IDs with real ones
# sourced from your domain expert (DJ / music curator).
# Multiple playlists per mood increase song variety.

MOOD_PLAYLISTS = {
    "happy":       ["37i9dQZF1DXdPec7aLTmlC"],
    "energetic":   ["37i9dQZF1DXdxcBWuJkbcy"],
    "motivated":   ["37i9dQZF1DX3rxVfibe1L0"],
    "confident":   ["37i9dQZF1DX2RxBh64BHjQ"],
    "angry":       ["37i9dQZF1DWWJOmJ7nRx0C"],
    "anxious":     ["37i9dQZF1DX3Ogo9pFvBkY"],
    "stressed":    ["37i9dQZF1DX4sWSpwq3LiO"],
    "sad":         ["37i9dQZF1DX7qK8ma5wgG1"],
    "melancholic": ["37i9dQZF1DX3YSRoSdA634"],
    "tired":       ["37i9dQZF1DX6ziVCJnEm59"],
    "bored":       ["37i9dQZF1DX4WYpdgoIcn6"],
    "calm":        ["37i9dQZF1DXbttv0GbQTNn"],
    "romantic":    ["37i9dQZF1DXbITWG1ZJKYt"],
    "nostalgic":   ["37i9dQZF1DX5Kpyebo1BOU"],
    "focused":     ["37i9dQZF1DX8NTLI2TtZa6"],
}


# ── Tier 3: Manual LyricTone Override Table ──────────────────
# KEs can override the automatic tone classification for any
# specific track by adding its Spotify track ID here.
# Format: "spotify_track_id": "lyric_tone_atom"
#
# Valid tone atoms:
#   positive | celebratory | motivational | hype | empowering |
#   assertive | aggressive | cathartic | soothing | neutral |
#   melancholic | reflective | bittersweet | calm |
#   romantic | intimate | instrumental
#
# To find a track ID: open the track on Spotify, click
# Share -> Copy Song Link. The ID is the last segment of the URL.
# e.g. https://open.spotify.com/track/4aebBr4JAihzJQR0CiIZJv
#                                               ^^^^^^^^^^^^^^^^^^^

LYRICTONE_OVERRIDES = {
    # Example entries — replace with real track IDs and tones:
    # "4aebBr4JAihzJQR0CiIZJv": "instrumental",   # Weightless
    # "3n3Ppam7vgaVa1iaRUIOKE": "melancholic",     # Someone Like You
}


# ── Tier 1: Quadrant-Based Tone Map ─────────────────────────
# Primary automatic classification based on the mood seed.
# Derived from the mood_profiles.pl LyricTones lists.

MOOD_PRIMARY_TONE = {
    "happy":       "positive",
    "energetic":   "hype",
    "motivated":   "motivational",
    "confident":   "assertive",
    "angry":       "aggressive",
    "anxious":     "soothing",
    "stressed":    "soothing",
    "sad":         "melancholic",
    "melancholic": "reflective",
    "tired":       "neutral",
    "bored":       "positive",
    "calm":        "soothing",
    "romantic":    "romantic",
    "nostalgic":   "reflective",
    "focused":     "neutral",
}


# ── Tier 2: Audio Feature Refinement ────────────────────────
# Automatically refines the Tier 1 tone using Spotify's
# audio features. Applied after quadrant mapping.
# KEs can adjust these thresholds if the domain expert
# identifies better boundaries.

def refine_tone_from_features(base_tone, valence, energy,
                               instrumentalness, speechiness):
    """
    Refines the base tone using Spotify audio features.

    Parameters
    ----------
    base_tone        : str   — Tier 1 tone from MOOD_PRIMARY_TONE
    valence          : float — Spotify valence (0.0–1.0)
    energy           : float — Spotify energy  (0.0–1.0)
    instrumentalness : float — Spotify instrumentalness (0.0–1.0)
    speechiness      : float — Spotify speechiness (0.0–1.0)

    Returns
    -------
    str — refined tone atom
    """

    # High instrumentalness overrides all other tones
    # Threshold 0.8 aligns with the lyric_compatible/3 rule
    # in inference_engine.pl
    if instrumentalness >= 0.8:
        return "instrumental"

    # High speechiness (>0.66) suggests spoken word / rap
    # Reclassify to hype if energy is also high
    if speechiness > 0.66 and energy >= 0.7:
        return "hype"

    # Celebratory: high valence + high energy + not already hype
    if valence >= 0.8 and energy >= 0.75 and base_tone == "positive":
        return "celebratory"

    # Empowering: motivational base + very high energy
    if base_tone == "motivational" and energy >= 0.85:
        return "empowering"

    # Cathartic: aggressive base + moderate valence
    # (some release, not pure aggression)
    if base_tone == "aggressive" and valence >= 0.25:
        return "cathartic"

    # Bittersweet: reflective base + moderate valence
    # (not purely sad — aligns with Taruffi & Koelsch 2014)
    if base_tone in ("reflective", "melancholic") and valence >= 0.3:
        return "bittersweet"

    # Intimate: romantic base + very low energy
    if base_tone == "romantic" and energy < 0.35:
        return "intimate"

    # Calm: soothing base + very low energy + low speechiness
    if base_tone == "soothing" and energy < 0.3 and speechiness < 0.1:
        return "calm"

    # Default: return base tone unchanged
    return base_tone


def classify_lyric_tone(track_id, mood, valence, energy,
                         instrumentalness, speechiness):
    """
    Full three-tier LyricTone classification.

    Tier 1: Quadrant-based mapping from mood seed
    Tier 2: Audio feature refinement
    Tier 3: Manual KE override (highest priority)
    """

    # Tier 3 — Manual override (checked first, highest priority)
    if track_id in LYRICTONE_OVERRIDES:
        return LYRICTONE_OVERRIDES[track_id]

    # Tier 1 — Quadrant base tone
    base_tone = MOOD_PRIMARY_TONE.get(mood, "neutral")

    # Tier 2 — Audio feature refinement
    refined_tone = refine_tone_from_features(
        base_tone, valence, energy, instrumentalness, speechiness
    )

    return refined_tone


# ── Sanitiser ────────────────────────────────────────────────
def sanitize(text):
    """Remove characters unsafe for Prolog string atoms."""
    return re.sub(r"['\"]", "", text).strip()


# ── Fetcher ──────────────────────────────────────────────────
def fetch_tracks_for_mood(mood, playlist_id, limit=30):
    """
    Fetches up to `limit` tracks from a Spotify playlist and
    returns them as tuples ready for Prolog fact generation.
    """
    results = []
    try:
        items = sp.playlist_tracks(playlist_id, limit=limit)["items"]
        track_ids = [
            item["track"]["id"]
            for item in items
            if item["track"] and item["track"]["id"]
        ]
        if not track_ids:
            return results

        features_list = sp.audio_features(track_ids)

        for item, features in zip(items, features_list):
            if not features:
                continue

            track   = item["track"]
            t_id    = track["id"]
            title   = sanitize(track["name"])
            artist  = sanitize(track["artists"][0]["name"])
            bpm     = round(features["tempo"])
            energy  = round(features["energy"],          2)
            instr   = round(features["instrumentalness"], 2)
            valence = round(features["valence"],          2)
            speech  = round(features["speechiness"],      2)

            tone = classify_lyric_tone(
                t_id, mood, valence, energy, instr, speech
            )

            results.append((t_id, title, artist, mood,
                            bpm, energy, instr, valence, tone))

    except Exception as e:
        print(f"  [ERROR] {mood} — {e}")

    return results


# ── Writer ───────────────────────────────────────────────────
def write_prolog_facts(all_tracks, output_path="songs_kb.pl"):
    """
    Writes all tracks as Prolog facts to songs_kb.pl.
    Deduplicates by track ID.
    """
    with open(output_path, "w") as f:
        f.write("%% ============================================================\n")
        f.write("%% MoodBeats — Song Knowledge Base\n")
        f.write("%% songs_kb.pl\n")
        f.write("%%\n")
        f.write("%% Auto-generated by spotify_to_prolog.py\n")
        f.write("%% DO NOT edit song attribute values manually —\n")
        f.write("%% re-run the bridge script to regenerate.\n")
        f.write("%%\n")
        f.write("%% To override a LyricTone, add the track ID to\n")
        f.write("%% LYRICTONE_OVERRIDES in spotify_to_prolog.py\n")
        f.write("%% and re-run. Do not edit this file directly.\n")
        f.write("%%\n")
        f.write("%% song(ID, Title, Artist, Genre, BPM,\n")
        f.write("%%      Energy, Instrumentalness, Valence, LyricTone).\n")
        f.write("%% ============================================================\n\n")

        seen   = set()
        count  = 0
        current_mood = None

        for track in all_tracks:
            t_id, title, artist, mood, bpm, energy, instr, valence, tone = track

            if t_id in seen:
                continue
            seen.add(t_id)
            count += 1

            # Section comment when mood changes
            if mood != current_mood:
                current_mood = mood
                f.write(f"\n%% ── {mood.upper()} ──\n")

            f.write(
                f"song('{t_id}', '{title}', '{artist}', "
                f"{mood}, {bpm}, {energy}, {instr}, {valence}, {tone}).\n"
            )

    print(f"\nWrote {count} unique tracks to {output_path}")


# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    all_tracks = []

    for mood, playlist_ids in MOOD_PLAYLISTS.items():
        mood_count = 0
        for pid in playlist_ids:
            tracks = fetch_tracks_for_mood(mood, pid)
            all_tracks.extend(tracks)
            mood_count += len(tracks)
        print(f"  [{mood:<12}] {mood_count} tracks fetched")

    write_prolog_facts(all_tracks)