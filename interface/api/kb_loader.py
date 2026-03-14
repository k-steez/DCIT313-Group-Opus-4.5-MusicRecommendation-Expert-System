import os
import re
from typing import List, Dict

from .models import Song


FACT_RE = re.compile(
    r"^song\('([^']+)',\s*'([^']*)',\s*'([^']*)',\s*"
    r"([a-zA-Z_][a-zA-Z0-9_]*)\s*,\s*([0-9]+)\s*,\s*"
    r"([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*"
    r"([a-zA-Z_][a-zA-Z0-9_]*)\)\.\s*$"
)


def load_songs_kb(path: str = "songs_kb.pl") -> List[Song]:
    """
    Parse songs_kb.pl into a list of Song objects.

    This mirrors the regex used in spotify-to-python.py so the
    API layer stays in sync with the KB writer.
    """
    songs: List[Song] = []
    if not os.path.exists(path):
        return songs

    with open(path, "r", encoding="utf-8") as f:
        
        for line in f:
            m = FACT_RE.match(line.strip())
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

            songs.append(
                Song(
                    id=t_id,
                    title=title,
                    artist=artist,
                    mood=mood,
                    bpm=int(bpm),
                    energy=float(energy),
                    instrumentalness=float(instr),
                    valence=float(valence),
                    lyric_tone=tone,
                )
            )

    return songs


def index_by_mood(songs: List[Song]) -> Dict[str, List[Song]]:
    """
    Group songs by mood for fast mood-based lookups.
    """
    by_mood: Dict[str, List[Song]] = {}
    for s in songs:
        by_mood.setdefault(s.mood, []).append(s)
    return by_mood

