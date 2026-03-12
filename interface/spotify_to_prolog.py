# ============================================================
# MoodBeats - Spotify to Prolog Bridge
# spotify_to_prolog.py
#
# Fetches tracks and audio features from Spotify and writes
# them as Prolog facts to knowledge_base/songs_kb.pl.
#
# LyricTone is determined by a three-tier resolution system:
#   Tier 1 - Valence + Energy quadrant mapping (automatic)
#   Tier 2 - Spotify audio feature refinement (automatic)
#   Tier 3 - Manual override table (KE-editable, see below)
#
# LyricComplexity (required by inference_engine.pl):
#   Derived automatically from instrumentalness + speechiness:
#     simple   if instrumentalness >= 0.7
#     complex  if speechiness >= 0.3
#     moderate otherwise
#
# Schema written:
#   song(ID, Title, Artist, BPM, Energy, Instrumentalness,
#        Valence, LyricTone, LyricComplexity).
#
# Setup:
#   1. pip install spotipy python-dotenv
#   2. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as
#      environment variables (or in interface/.env)
#   3. Replace playlist IDs in MOOD_PLAYLISTS with real IDs
#   4. Run: python spotify_to_prolog.py
#      Output is written to ../knowledge_base/songs_kb.pl
# ============================================================

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv not installed; rely on environment variables

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# -- Credentials (read from environment, never hardcoded) ----
CLIENT_ID     = os.environ.get("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError(
        "Missing Spotify credentials.\n"
        "Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables,\n"
        "or create interface/.env with those keys."
    )

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
))

# -- Output path ---------------------------------------------
OUTPUT_PATH = (
    Path(__file__).parent / ".." / "knowledge_base" / "songs_kb.pl"
).resolve()


# -- Mood-to-Playlist Seed Map -------------------------------
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


# -- Tier 3: Manual LyricTone Override Table -----------------
# KEs can override the automatic tone classification for any
# specific track by adding its Spotify track ID here.
# Format: "spotify_track_id": "lyric_tone_atom"
LYRICTONE_OVERRIDES: dict[str, str] = {
    # Example:
    # "4aebBr4JAihzJQR0CiIZJv": "instrumental",  # Weightless
}


# -- Tier 1: Quadrant-Based Tone Map -------------------------
MOOD_PRIMARY_TONE = {
    "happy": "positive", "energetic": "hype", "motivated": "motivational",
    "confident": "assertive", "angry": "aggressive", "anxious": "soothing",
    "stressed": "soothing", "sad": "melancholic", "melancholic": "reflective",
    "tired": "neutral", "bored": "positive", "calm": "soothing",
    "romantic": "romantic", "nostalgic": "reflective", "focused": "neutral",
}


def refine_tone_from_features(base_tone, valence, energy, instrumentalness, speechiness):
    if instrumentalness >= 0.8:
        return "instrumental"
    if speechiness > 0.66 and energy >= 0.7:
        return "hype"
    if valence >= 0.8 and energy >= 0.75 and base_tone == "positive":
        return "celebratory"
    if base_tone == "motivational" and energy >= 0.85:
        return "empowering"
    if base_tone == "aggressive" and valence >= 0.25:
        return "cathartic"
    if base_tone in ("reflective", "melancholic") and valence >= 0.3:
        return "bittersweet"
    if base_tone == "romantic" and energy < 0.35:
        return "intimate"
    if base_tone == "soothing" and energy < 0.3 and speechiness < 0.1:
        return "calm"
    return base_tone


def classify_lyric_tone(track_id, mood, valence, energy, instrumentalness, speechiness):
    if track_id in LYRICTONE_OVERRIDES:
        return LYRICTONE_OVERRIDES[track_id]
    base_tone = MOOD_PRIMARY_TONE.get(mood, "neutral")
    return refine_tone_from_features(base_tone, valence, energy, instrumentalness, speechiness)


def classify_lyric_complexity(instrumentalness, speechiness):
    """Derive LyricComplexity: simple | complex | moderate"""
    if instrumentalness >= 0.7:
        return "simple"
    if speechiness >= 0.3:
        return "complex"
    return "moderate"


def sanitize(text):
    """Escape single quotes for Prolog atoms."""
    return text.replace("'", "''").strip()


def fetch_tracks_for_mood(mood, playlist_id, limit=30):
    results = []
    try:
        items = sp.playlist_tracks(playlist_id, limit=limit)["items"]
        track_ids = [
            item["track"]["id"]
            for item in items
            if item.get("track") and item["track"].get("id")
        ]
        if not track_ids:
            return results
        features_list = sp.audio_features(track_ids)
        for item, features in zip(items, features_list):
            if not features:
                continue
            track  = item["track"]
            t_id   = track["id"]
            title  = sanitize(track["name"])
            artist = sanitize(track["artists"][0]["name"])
            bpm    = round(features["tempo"])
            energy = round(features["energy"], 2)
            instr  = round(features["instrumentalness"], 2)
            valence = round(features["valence"], 2)
            speech  = round(features["speechiness"], 2)
            tone       = classify_lyric_tone(t_id, mood, valence, energy, instr, speech)
            complexity = classify_lyric_complexity(instr, speech)
            results.append((t_id, title, artist, bpm, energy, instr, valence, tone, complexity))
    except Exception as e:
        print(f"  [ERROR] {mood} - {e}")
    return results


def write_prolog_facts(all_tracks, output_path=OUTPUT_PATH):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("%% MoodBeats - Song Knowledge Base (auto-generated)\n")
        f.write("%% song(ID, Title, Artist, BPM, Energy, Instrumentalness,\n")
        f.write("%%      Valence, LyricTone, LyricComplexity).\n\n")
        seen = set()
        count = 0
        for track in all_tracks:
            t_id, title, artist, bpm, energy, instr, valence, tone, complexity = track
            if t_id in seen:
                continue
            seen.add(t_id)
            count += 1
            f.write(
                f"song('{t_id}', '{title}', '{artist}', "
                f"{bpm}, {energy}, {instr}, {valence}, {tone}, {complexity}).\n"
            )
    print(f"\nWrote {count} unique tracks to {output_path}")


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
    print("\nDone. Restart the MoodBeats backend to load the new knowledge base.")
