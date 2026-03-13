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
from spotipy.oauth2 import SpotifyOAuth
import re
import os
from collections import defaultdict
from dotenv import load_dotenv

# Credentials
# Load environment variables from a .env file (if present)
load_dotenv()


def get_spotify_client():
    """
    Returns a Spotipy client authorised with a USER token
    via OAuth2 Authorization Code Flow.

    - On first run, opens the browser and asks you to log in.
    - Caches the token in a .cache file so subsequent runs
      reuse the token until it expires.

    Expected environment variables (in .env):
      SPOTIPY_CLIENT_ID
      SPOTIPY_CLIENT_SECRET
      SPOTIPY_REDIRECT_URI
    """
    scope = (
        "playlist-read-private "
        "playlist-read-collaborative "
        "user-library-read"
    )

    auth_manager = SpotifyOAuth(scope=scope)

    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=10,
        retries=3,
    )


# Global Spotify client using user OAuth
sp = get_spotify_client()


# ── Mood Search Queries ──────────────────────────────────────
# Defines natural language search queries to find appropriate
# playlists for each mood dynamically via the Spotify Search API.
# The hardcoded IDs are kept as an emergency fallback.

MOOD_SEARCH_QUERIES = {
    # Core moods
    "happy":         "happy hits feel good",
    "energetic":     "energetic workout hype",
    "motivated":     "motivation focus empowering",
    "confident":     "confidence boost swagger",
    "angry":         "angry gym aggro",
    "anxious":       "soothing anxiety relief deep breath",
    "stressed":      "stress relief calm down relax",
    "sad":           "sad songs heartbreak crying",
    "melancholic":   "melancholy moody reflection bittersweet",
    "tired":         "sleep sleepy calm relaxing",
    "bored":         "bored upbeat pop fun",
    "calm":          "calm relaxing chill vibes",
    "romantic":      "romantic romance love songs",
    "nostalgic":     "nostalgia throwback classics memories",
    "focused":       "deep focus study beats instrumental",

    # Extra mood flavours to broaden coverage
    "happy_chill":   "chill happy acoustic",
    "happy_upbeat":  "summer upbeat happy pop",
    "study_focus":   "deep focus concentration no lyrics",
    "study_lofi":    "lofi study beats chillhop",
    "sleep":         "sleep ambient calm",
    "workout_hard":  "hard workout gym power",
    "party":         "party hits dance pop",
    "roadtrip":      "road trip driving songs",
    "piano_relax":   "relaxing piano calm",
    "chillhop":      "chillhop lofi beats",

    # Extra categories for broader coverage
    "lofi_chill":       "lofi chill beats study",
    "deep_focus_tech":  "techno deep focus minimal",
    "jazz_chill":       "chill jazz evening",
    "classical_focus":  "classical piano study focus",
    "gospel_praise":    "gospel praise worship",
    "afrobeats_party":  "afrobeats party dance",
    "hiphop_confident": "hip hop confidence swagger",
    "indie_sad":        "indie sad acoustic heartbreak",
}

# Fallback static IDs if search fails
MOOD_PLAYLISTS_FALLBACK = {
    # Core moods – official editorial playlists
    "happy":         ["37i9dQZF1DXdPec7aLTmlC"],
    "energetic":     ["37i9dQZF1DXdxcBWuJkbcy"],
    "motivated":     ["37i9dQZF1DX3rxVfibe1L0"],
    "confident":     ["37i9dQZF1DX2RxBh64BHjQ"],
    "angry":         ["37i9dQZF1DWWJOmJ7nRx0C"],
    "anxious":       ["37i9dQZF1DX3Ogo9pFvBkY"],
    "stressed":      ["37i9dQZF1DX4sWSpwq3LiO"],
    "sad":           ["37i9dQZF1DX7qK8ma5wgG1"],
    "melancholic":   ["37i9dQZF1DX3YSRoSdA634"],
    "tired":         ["37i9dQZF1DX6ziVCJnEm59"],
    "bored":         ["37i9dQZF1DX4WYpdgoIcn6"],
    "calm":          ["37i9dQZF1DXbttv0GbQTNn"],
    "romantic":      ["37i9dQZF1DXbITWG1ZJKYt"],
    "nostalgic":     ["37i9dQZF1DX5Kpyebo1BOU"],
    "focused":       ["37i9dQZF1DX8NTLI2TtZa6"],

    # Extra moods – reuse solid playlists as safe fallbacks
    # (search will normally find additional playlists anyway)
    "happy_chill":   ["37i9dQZF1DX4WYpdgoIcn6"],  # happy & fun
    "happy_upbeat":  ["37i9dQZF1DXdPec7aLTmlC"],
    "study_focus":   ["37i9dQZF1DX8NTLI2TtZa6"],
    "study_lofi":    ["37i9dQZF1DX8NTLI2TtZa6"],
    "sleep":         ["37i9dQZF1DX4sWSpwq3LiO"],
    "workout_hard":  ["37i9dQZF1DXdxcBWuJkbcy"],
    "party":         ["37i9dQZF1DX4WYpdgoIcn6"],
    "roadtrip":      ["37i9dQZF1DX4WYpdgoIcn6"],
    "piano_relax":   ["37i9dQZF1DXbttv0GbQTNn"],
    "chillhop":      ["37i9dQZF1DX8NTLI2TtZa6"],

    # Extra categories – reuse solid fallbacks
    "lofi_chill":       ["37i9dQZF1DX8NTLI2TtZa6"],
    "deep_focus_tech":  ["37i9dQZF1DX8NTLI2TtZa6"],
    "jazz_chill":       ["37i9dQZF1DXbttv0GbQTNn"],
    "classical_focus":  ["37i9dQZF1DX8NTLI2TtZa6"],
    "gospel_praise":    ["37i9dQZF1DXdPec7aLTmlC"],
    "afrobeats_party":  ["37i9dQZF1DX4WYpdgoIcn6"],
    "hiphop_confident": ["37i9dQZF1DX2RxBh64BHjQ"],
    "indie_sad":        ["37i9dQZF1DX7qK8ma5wgG1"],
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
    # Core moods
    "happy":         "positive",
    "energetic":     "hype",
    "motivated":     "motivational",
    "confident":     "assertive",
    "angry":         "aggressive",
    "anxious":       "soothing",
    "stressed":      "soothing",
    "sad":           "melancholic",
    "melancholic":   "reflective",
    "tired":         "neutral",
    "bored":         "positive",
    "calm":          "soothing",
    "romantic":      "romantic",
    "nostalgic":     "reflective",
    "focused":       "neutral",

    # Extra moods – mapped onto existing tone quadrants
    "happy_chill":   "positive",
    "happy_upbeat":  "positive",
    "study_focus":   "neutral",
    "study_lofi":    "neutral",
    "sleep":         "calm",
    "workout_hard":  "hype",
    "party":         "celebratory",
    "roadtrip":      "positive",
    "piano_relax":   "soothing",
    "chillhop":      "neutral",

    # Extra categories
    "lofi_chill":       "neutral",
    "deep_focus_tech":  "neutral",
    "jazz_chill":       "soothing",
    "classical_focus":  "neutral",
    "gospel_praise":    "celebratory",
    "afrobeats_party":  "celebratory",
    "hiphop_confident": "assertive",
    "indie_sad":        "melancholic",
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


# ── Fallback feature profiles (no audio_features) ───────────
# When the audio-features endpoint is blocked (403 in Dev Mode),
# we approximate numeric features from the mood itself so that
# the expert system still has a usable knowledge base.

DEFAULT_FEATURE_PROFILE = {
    # Core moods
    "happy":         dict(bpm=120, energy=0.85, instr=0.0, valence=0.9,  speech=0.05),
    "energetic":     dict(bpm=135, energy=0.95, instr=0.0, valence=0.75, speech=0.08),
    "motivated":     dict(bpm=130, energy=0.9,  instr=0.0, valence=0.8,  speech=0.06),
    "confident":     dict(bpm=125, energy=0.9,  instr=0.0, valence=0.7,  speech=0.07),
    "angry":         dict(bpm=140, energy=0.95, instr=0.0, valence=0.3,  speech=0.05),
    "anxious":       dict(bpm=95,  energy=0.45, instr=0.1, valence=0.3,  speech=0.04),
    "stressed":      dict(bpm=90,  energy=0.4,  instr=0.1, valence=0.35, speech=0.04),
    "sad":           dict(bpm=80,  energy=0.3,  instr=0.1, valence=0.2,  speech=0.03),
    "melancholic":   dict(bpm=85,  energy=0.35, instr=0.2, valence=0.25, speech=0.03),
    "tired":         dict(bpm=75,  energy=0.3,  instr=0.1, valence=0.4,  speech=0.03),
    "bored":         dict(bpm=110, energy=0.6,  instr=0.0, valence=0.6,  speech=0.05),
    "calm":          dict(bpm=70,  energy=0.25, instr=0.3, valence=0.5,  speech=0.02),
    "romantic":      dict(bpm=90,  energy=0.4,  instr=0.1, valence=0.8,  speech=0.03),
    "nostalgic":     dict(bpm=95,  energy=0.45, instr=0.1, valence=0.5,  speech=0.03),
    "focused":       dict(bpm=100, energy=0.5,  instr=0.4, valence=0.55, speech=0.02),

    # Extra moods – tuned variants around the core profiles
    "happy_chill":   dict(bpm=110, energy=0.75, instr=0.1, valence=0.9,  speech=0.03),
    "happy_upbeat":  dict(bpm=130, energy=0.9,  instr=0.0, valence=0.9,  speech=0.06),
    "study_focus":   dict(bpm=95,  energy=0.45, instr=0.5, valence=0.55, speech=0.02),
    "study_lofi":    dict(bpm=90,  energy=0.4,  instr=0.6, valence=0.5,  speech=0.02),
    "sleep":         dict(bpm=65,  energy=0.2,  instr=0.7, valence=0.5,  speech=0.01),
    "workout_hard":  dict(bpm=145, energy=0.98, instr=0.0, valence=0.7,  speech=0.05),
    "party":         dict(bpm=128, energy=0.95, instr=0.0, valence=0.85, speech=0.06),
    "roadtrip":      dict(bpm=115, energy=0.7,  instr=0.1, valence=0.75, speech=0.05),
    "piano_relax":   dict(bpm=70,  energy=0.25, instr=0.8, valence=0.55, speech=0.01),
    "chillhop":      dict(bpm=92,  energy=0.5,  instr=0.6, valence=0.6,  speech=0.02),

    # Extra categories
    "lofi_chill":       dict(bpm=88,  energy=0.4,  instr=0.7, valence=0.55, speech=0.02),
    "deep_focus_tech":  dict(bpm=125, energy=0.7,  instr=0.6, valence=0.6,  speech=0.01),
    "jazz_chill":       dict(bpm=80,  energy=0.35, instr=0.6, valence=0.6,  speech=0.02),
    "classical_focus":  dict(bpm=72,  energy=0.25, instr=0.9, valence=0.55, speech=0.01),
    "gospel_praise":    dict(bpm=120, energy=0.85, instr=0.1, valence=0.9,  speech=0.05),
    "afrobeats_party":  dict(bpm=115, energy=0.9,  instr=0.1, valence=0.85, speech=0.06),
    "hiphop_confident": dict(bpm=95,  energy=0.8,  instr=0.1, valence=0.7,  speech=0.20),
    "indie_sad":        dict(bpm=82,  energy=0.4,  instr=0.2, valence=0.3,  speech=0.03),
}


# ── Fetcher ──────────────────────────────────────────────────
def find_playlists_for_mood(mood, limit=1):
    """
    Dynamically searches for playlists matching the mood's query.
    Returns a list of playlist IDs.
    """
    query = MOOD_SEARCH_QUERIES.get(mood, mood)
    try:
        results = sp.search(q=query, type="playlist", limit=limit + 5)
        playlist_ids = []
        if results and 'playlists' in results and 'items' in results['playlists']:
            for item in results['playlists']['items']:
                if item and 'id' in item:
                    # Prefer playlists that aren't terribly short
                    if item.get('tracks', {}).get('total', 0) > 10:
                        playlist_ids.append(item['id'])
                if len(playlist_ids) >= limit:
                    break
        
        if playlist_ids:
            return playlist_ids
            
    except Exception as e:
        print(f"  [ERROR] Search failed for {mood} - {e}")
        
    print(f"  [WARN] Falling back to static IDs for {mood}")
    return MOOD_PLAYLISTS_FALLBACK.get(mood, [])
def fetch_tracks_for_mood(mood, playlist_id, limit=100):
    """
    Fetches up to `limit` tracks from a Spotify playlist and
    returns:
        - a list of track tuples ready for Prolog fact generation
        - a set of artist IDs seen in this playlist

    Increasing `limit` or calling this repeatedly with more
    playlists is what lets you keep growing songs_kb.pl over
    multiple runs; dedup happens later by track ID.
    """
    results = []
    artist_ids = set()
    try:
        items = sp.playlist_tracks(playlist_id=playlist_id, limit=limit)["items"]

        track_ids = []
        for item in items:
            track = item.get("track")
            if not track or not track.get("id"):
                continue
            track_ids.append(track["id"])
            if track.get("artists"):
                primary_artist = track["artists"][0]
                if primary_artist and primary_artist.get("id"):
                    artist_ids.add(primary_artist["id"])
        if not track_ids:
            return results

        # Try to fetch real audio features. If this endpoint is blocked
        # (403 in Dev Mode), fall back to mood-based defaults so that
        # we still populate the knowledge base.
        features_list = []
        try:
            features_list = sp.audio_features(track_ids)
        except Exception as e:
            print(f"  [WARN] audio_features blocked for {mood} — {e}")
            features_list = [None] * len(track_ids)

        for item, features in zip(items, features_list):
            track = item["track"]
            if not track:
                continue

            t_id   = track["id"]
            title  = sanitize(track["name"])
            artist = sanitize(track["artists"][0]["name"])

            if features:
                bpm     = round(features["tempo"])
                energy  = round(features["energy"],           2)
                instr   = round(features["instrumentalness"], 2)
                valence = round(features["valence"],          2)
                speech  = round(features["speechiness"],      2)
            else:
                # Use heuristic defaults derived from the mood profile.
                profile = DEFAULT_FEATURE_PROFILE.get(mood, DEFAULT_FEATURE_PROFILE["focused"])
                bpm     = profile["bpm"]
                energy  = profile["energy"]
                instr   = profile["instr"]
                valence = profile["valence"]
                speech  = profile["speech"]

            tone = classify_lyric_tone(
                t_id, mood, valence, energy, instr, speech
            )

            results.append((t_id, title, artist, mood,
                            bpm, energy, instr, valence, tone))

    except Exception as e:
        print(f"  [ERROR] {mood} — {e}")

    return results, artist_ids


def expand_tracks_from_artists(artist_ids_by_mood, per_mood_cap=10, albums_per_artist=3):
    """
    Expands the dataset by walking the graph:
        mood → artists (from playlists) → artist albums → album tracks.

    This is a lightweight implementation of the "graph crawler"
    idea that stays within allowed endpoints:
      - /v1/artists/{id}/albums
      - /v1/albums/{id}/tracks

    We cap the number of artists and albums per artist to avoid
    explosive growth or hitting rate limits too quickly.
    """
    extra_tracks = []

    for mood, artist_ids in artist_ids_by_mood.items():
        # Cap the number of artists we expand per mood
        selected_artists = list(artist_ids)[:per_mood_cap]
        if not selected_artists:
            continue

        print(f"  [INFO] Expanding artists for mood={mood} (up to {len(selected_artists)} artists)")

        for artist_id in selected_artists:
            try:
                albums = sp.artist_albums(
                    artist_id,
                    limit=albums_per_artist,
                    album_type="album,single",
                ).get("items", [])
            except Exception as e:
                print(f"    [WARN] artist_albums failed for {artist_id} — {e}")
                continue

            for album in albums:
                album_id = album.get("id")
                if not album_id:
                    continue

                try:
                    album_tracks = sp.album_tracks(album_id).get("items", [])
                except Exception as e:
                    print(f"    [WARN] album_tracks failed for {album_id} — {e}")
                    continue

                for track in album_tracks:
                    if not track or not track.get("id"):
                        continue

                    t_id = track["id"]
                    title = sanitize(track.get("name", ""))
                    artists = track.get("artists") or []
                    artist_name = sanitize(artists[0]["name"]) if artists else "Unknown"

                    profile = DEFAULT_FEATURE_PROFILE.get(mood, DEFAULT_FEATURE_PROFILE["focused"])
                    bpm     = profile["bpm"]
                    energy  = profile["energy"]
                    instr   = profile["instr"]
                    valence = profile["valence"]
                    speech  = profile["speech"]

                    tone = classify_lyric_tone(
                        t_id, mood, valence, energy, instr, speech
                    )

                    extra_tracks.append(
                        (t_id, title, artist_name, mood,
                         bpm, energy, instr, valence, tone)
                    )

    return extra_tracks


def search_tracks_for_mood(mood, query, pages=20, page_size=10, start_page=0):
    """
    Searches Spotify directly for TRACKS that match the mood query.

    - page_size is clamped to 10 (per Spotify Search API docs: limit 0–10).
    - start_page skips the first N result pages so later runs can "go deeper"
      and discover new track IDs instead of re-fetching the same top results.

    Each returned track is labelled with `mood`, given numeric features from
    DEFAULT_FEATURE_PROFILE[mood], and LyricTone via classify_lyric_tone.
    """
    all_items = []

    # Clamp to allowed API range 1–10
    page_size = max(1, min(page_size, 10))

    for i in range(pages):
        page = start_page + i
        offset = page * page_size
        try:
            results = sp.search(
                q=query,
                type="track",
                limit=page_size,
                offset=offset,
            )
        except Exception as e:
            print(f"[WARN] track search failed for mood={mood}, offset={offset} — {e}")
            break

        tracks = (results.get("tracks") or {}).get("items") or []
        if not tracks:
            break

        all_items.extend(tracks)

    # Use the heuristic audio profile for this mood
    profile = DEFAULT_FEATURE_PROFILE.get(mood, DEFAULT_FEATURE_PROFILE["focused"])
    bpm     = profile["bpm"]
    energy  = profile["energy"]
    instr   = profile["instr"]
    valence = profile["valence"]
    speech  = profile["speech"]

    kb_tracks = []

    for track in all_items:
        if not track or not track.get("id"):
            continue

        t_id = track["id"]
        title = sanitize(track.get("name", ""))
        artists = track.get("artists") or []
        artist_name = sanitize(artists[0]["name"]) if artists else "Unknown"

        tone = classify_lyric_tone(
            t_id,
            mood,
            valence,
            energy,
            instr,
            speech,
        )

        kb_tracks.append(
            (t_id, title, artist_name, mood,
             bpm, energy, instr, valence, tone)
        )

    return kb_tracks


# ── Writer ───────────────────────────────────────────────────
def write_prolog_facts(all_tracks, output_path="songs_kb.pl"):
    """
    Writes all tracks as Prolog facts to songs_kb.pl.

    Behaviour:
    - If songs_kb.pl already exists, existing facts are loaded first.
    - New tracks are merged *by track ID*:
        - If a track ID already exists, the newly fetched tuple
          overrides the old one (updated attributes win).
        - If a track ID is new, it is appended.
    - The merged set is then written back out, so we effectively
      "add newly fetched songs and override existing ones".
    """

    # ── Load existing facts (if any) ─────────────────────────
    existing_by_id = {}
    if os.path.exists(output_path):
        fact_re = re.compile(
            r"^song\('([^']+)',\s*'([^']*)',\s*'([^']*)',\s*"
            r"([a-zA-Z_][a-zA-Z0-9_]*)\s*,\s*([0-9]+)\s*,\s*"
            r"([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*"
            r"([a-zA-Z_][a-zA-Z0-9_]*)\)\.\s*$"
        )
        try:
            with open(output_path, "r") as f_in:
                for line in f_in:
                    m = fact_re.match(line.strip())
                    if not m:
                        continue
                    (
                        t_id,
                        title,
                        artist,
                        mood,
                        bpm,
                        energy,
                        instr,
                        valence,
                        tone,
                    ) = m.groups()
                    existing_by_id[t_id] = (
                        t_id,
                        title,
                        artist,
                        mood,
                        int(bpm),
                        float(energy),
                        float(instr),
                        float(valence),
                        tone,
                    )
        except Exception as e:
            print(f"[WARN] Failed to read existing {output_path}: {e}")

    # ── Merge with newly fetched tracks ───────────────────────
    for track in all_tracks:
        t_id = track[0]
        existing_by_id[t_id] = track

    merged_tracks = list(existing_by_id.values())

    # ── Write merged facts back to disk ───────────────────────
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

        for track in merged_tracks:
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


def load_existing_kb_index(output_path="songs_kb.pl"):
    """
    Reads the existing songs_kb.pl and returns:
      - existing_ids: set of all track IDs already in the KB
      - per_mood_counts: dict[mood] -> how many tracks currently labeled with that mood

    Used so each run can start searching from a later page per mood (start_page)
    and avoid re-adding the same IDs (global dedupe).
    """
    existing_ids = set()
    per_mood_counts = defaultdict(int)

    if not os.path.exists(output_path):
        return existing_ids, per_mood_counts

    fact_re = re.compile(
        r"^song\('([^']+)',\s*'([^']*)',\s*'([^']*)',\s*"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\s*,\s*([0-9]+)\s*,\s*"
        r"([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\)\.\s*$"
    )

    try:
        with open(output_path, "r") as f_in:
            for line in f_in:
                m = fact_re.match(line.strip())
                if not m:
                    continue
                t_id = m.group(1)
                mood = m.group(4)
                existing_ids.add(t_id)
                per_mood_counts[mood] += 1
    except Exception as e:
        print(f"[WARN] Failed to index existing {output_path}: {e}")

    return existing_ids, per_mood_counts


# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    # 0) Index existing KB so we know what we already have
    existing_ids, per_mood_counts = load_existing_kb_index("songs_kb.pl")

    all_tracks = []
    seen_ids = set(existing_ids)  # global dedupe including previous runs

    TARGET_TOTAL = 10000          # soft global cap for the whole KB
    PAGES_PER_MOOD = 20           # 20 * 10 = up to 200 candidates per mood per run
    PAGE_SIZE = 10                # must be <= 10 per Spotify Search docs

    print(f"[INFO] Existing KB: {len(existing_ids)} tracks")

    for mood, query in MOOD_SEARCH_QUERIES.items():
        already_for_mood = per_mood_counts.get(mood, 0)
        # How many pages of size PAGE_SIZE we have effectively "covered" so far
        start_page = already_for_mood // PAGE_SIZE

        print(
            f"\n[Mood] {mood} — searching tracks: '{query}' "
            f"(already in KB for this mood: {already_for_mood}, start_page={start_page})"
        )

        kb_tracks = search_tracks_for_mood(
            mood,
            query,
            pages=PAGES_PER_MOOD,
            page_size=PAGE_SIZE,
            start_page=start_page,
        )

        mood_added = 0
        for t in kb_tracks:
            t_id = t[0]
            if t_id in seen_ids:
                continue
            seen_ids.add(t_id)
            all_tracks.append(t)
            mood_added += 1

            if len(seen_ids) >= TARGET_TOTAL:
                break

        print(
            f"  [Summary] {mood}: {mood_added} NEW unique tracks added "
            f"(global total now = {len(seen_ids)})"
        )

        if len(seen_ids) >= TARGET_TOTAL:
            print("\n[INFO] Target total reached, stopping early.")
            break

    print(f"\n[GLOBAL] NEW tracks fetched this run: {len(all_tracks)}")

    # Merge only the newcomers with the existing KB
    write_prolog_facts(all_tracks)