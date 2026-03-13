from typing import List, Dict
import random

from fastapi import FastAPI, HTTPException, Query

from .models import Song
from .kb_loader import load_songs_kb, index_by_mood


app = FastAPI(title="MoodBeats API", version="1.0.0")


ALL_SONGS: List[Song] = []
SONGS_BY_MOOD: Dict[str, List[Song]] = {}


@app.on_event("startup")
def startup_load_kb() -> None:
    """
    Load songs_kb.pl into memory once when the API process starts.
    """
    global ALL_SONGS, SONGS_BY_MOOD

    ALL_SONGS = load_songs_kb("songs_kb.pl")
    SONGS_BY_MOOD = index_by_mood(ALL_SONGS)

    print(f"[MoodBeats API] Loaded {len(ALL_SONGS)} songs into memory")


@app.get("/api/moods")
def list_moods():
    """
    List all moods present in the KB with their song counts.
    """
    return [
        {"mood": mood, "count": len(songs)}
        for mood, songs in sorted(SONGS_BY_MOOD.items(), key=lambda x: x[0])
    ]


@app.get("/api/recommendations", response_model=List[Song])
def get_recommendations(
    mood: str = Query(..., description="Mood atom, e.g. happy, sad, study_lofi"),
    limit: int = Query(20, ge=1, le=100, description="Max number of songs to return"),
    shuffle: bool = Query(True, description="Shuffle before slicing"),
) -> List[Song]:
    """
    Main endpoint: return up to `limit` songs aligned to a given mood.

    Strategy:
      - Filter songs by `mood`
      - Optionally shuffle for variety
      - Slice to `limit`
    """
    if mood not in SONGS_BY_MOOD:
        raise HTTPException(status_code=404, detail=f"Unknown mood: {mood}")

    candidates = SONGS_BY_MOOD[mood].copy()
    if shuffle:
        random.shuffle(candidates)

    return candidates[:limit]


@app.get("/api/songs/{song_id}", response_model=Song)
def get_song(song_id: str) -> Song:
    """
    Fetch a single song by ID (for details page or debugging).
    """
    for s in ALL_SONGS:
        if s.id == song_id:
            return s

    raise HTTPException(status_code=404, detail="Song not found")

