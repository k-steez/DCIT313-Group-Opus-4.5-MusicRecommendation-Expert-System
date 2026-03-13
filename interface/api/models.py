from pydantic import BaseModel


class Song(BaseModel):
    """
    Shape of a single song fact exposed to the frontend.

    Mirrors:
      song(ID, Title, Artist, Mood, BPM,
           Energy, Instrumentalness, Valence, LyricTone).
    """

    id: str
    title: str
    artist: str
    mood: str
    bpm: int
    energy: float
    instrumentalness: float
    valence: float
    lyric_tone: str

