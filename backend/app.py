"""
MoodBeats — Flask REST API
app.py

Endpoints:
  GET  /api/health               Health check
  GET  /api/moods                List all available mood atoms
  GET  /api/activities           List all available activity atoms
  GET  /api/cognitive-loads      List valid cognitive load values
  POST /api/recommend            Run the expert system
  GET  /api/songs                List all songs in the knowledge base
  POST /api/songs/rebuild        Trigger songs_kb.pl rebuild (requires Spotify creds)

All POST bodies and responses are JSON.
CORS is enabled for all origins (development; restrict in production).
"""

import os
import subprocess
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent to path so prolog_bridge is importable when running directly
sys.path.insert(0, str(Path(__file__).parent))

import prolog_bridge as pb

app = Flask(__name__)
CORS(app)  # Allow React dev server on a different port

# ── Helpers ───────────────────────────────────────────────────

def _ok(data: dict, status: int = 200):
    return jsonify({"status": "ok", **data}), status


def _err(message: str, status: int = 400):
    return jsonify({"status": "error", "message": message}), status


# ── Routes ────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """Basic health/liveness probe."""
    return _ok({"service": "MoodBeats Expert System API", "version": "1.0.0"})


@app.route("/api/moods", methods=["GET"])
def list_moods():
    """Return all 15 mood atoms available in the knowledge base."""
    return _ok({"moods": pb.get_moods()})


@app.route("/api/activities", methods=["GET"])
def list_activities():
    """Return all 12 activity atoms available in the knowledge base."""
    return _ok({"activities": pb.get_activities()})


@app.route("/api/cognitive-loads", methods=["GET"])
def list_cognitive_loads():
    """Return the three cognitive load values: high, moderate, low."""
    return _ok({"cognitive_loads": pb.get_cognitive_loads()})


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Run the expert system and return a personalised playlist.

    Request body (JSON):
    {
        "mood":           string,   // one of VALID_MOODS
        "activity":       string,   // one of VALID_ACTIVITIES
        "cognitive_load": string,   // "high" | "moderate" | "low"
        "playlist_size":  int       // optional, default 10
    }

    Response body (JSON):
    {
        "status": "ok",
        "mood": ..., "activity": ..., "cognitive_load": ...,
        "playlist": [ { id, title, artist, bpm, energy, instrumentalness,
                         valence, tone, lyric_complexity }, ... ],
        "explanations": [ { id, title, artist, valence, energy, bpm, tone,
                             lyric_complexity, mood_valence_range,
                             mood_energy_range, mood_tones, activity_bpm_range,
                             valence_in_range, energy_in_range, tone_compatible,
                             bpm_in_range, lyric_compatible }, ... ],
        "fallback": bool,
        "fallback_message": string | null
    }
    """
    body = request.get_json(silent=True) or {}

    mood = body.get("mood", "")
    activity = body.get("activity", "")
    cognitive_load = body.get("cognitive_load", "moderate")
    playlist_size = int(body.get("playlist_size", 10))

    if not mood:
        return _err("Missing required field: 'mood'")
    if not activity:
        return _err("Missing required field: 'activity'")
    if playlist_size < 1 or playlist_size > 50:
        return _err("'playlist_size' must be between 1 and 50")

    try:
        result = pb.recommend(mood, activity, cognitive_load, playlist_size)
    except ValueError as exc:
        return _err(str(exc))
    except RuntimeError as exc:
        return _err(f"Prolog engine error: {exc}", status=500)
    except Exception as exc:
        return _err(f"Internal error: {exc}", status=500)

    return _ok(result)


@app.route("/api/songs", methods=["GET"])
def list_songs():
    """Return all songs currently in the knowledge base."""
    try:
        songs = pb.get_all_songs()
        return _ok({"songs": songs, "count": len(songs)})
    except Exception as exc:
        return _err(f"Error fetching songs: {exc}", status=500)


@app.route("/api/songs/rebuild", methods=["POST"])
def rebuild_songs():
    """
    Trigger a rebuild of songs_kb.pl from Spotify.

    Reads Spotify credentials from environment:
      SPOTIFY_CLIENT_ID
      SPOTIFY_CLIENT_SECRET

    The rebuild script is interface/spotify_to_prolog.py.
    After completion, the Prolog engine is reloaded.
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        return _err(
            "Spotify credentials not configured. "
            "Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.",
            status=503,
        )

    script_path = (
        Path(__file__).parent / ".." / "interface" / "spotify_to_prolog.py"
    ).resolve()

    if not script_path.exists():
        return _err(f"Rebuild script not found at {script_path}", status=500)

    env = {
        **os.environ,
        "SPOTIFY_CLIENT_ID": client_id,
        "SPOTIFY_CLIENT_SECRET": client_secret,
    }

    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        if proc.returncode != 0:
            return _err(
                f"Rebuild script failed:\n{proc.stderr[:1000]}",
                status=500,
            )
        # Reload so new songs are available immediately
        pb.reload_knowledge_base()
        return _ok({"message": "songs_kb.pl rebuilt successfully", "output": proc.stdout[:2000]})
    except subprocess.TimeoutExpired:
        return _err("Rebuild timed out (>120 s)", status=504)
    except Exception as exc:
        return _err(f"Rebuild error: {exc}", status=500)


# ── Dev server ────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print(f"[MoodBeats] Starting API server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
