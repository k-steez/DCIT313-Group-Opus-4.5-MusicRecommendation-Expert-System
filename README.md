# DCIT313-Group-Opus-4.5-MusicRecommendation-Expert-System

## Group members:
1. Jarawura Williams Koyiri - 22013675
2. Commey Jude Nii Klemesu - 22043189
3. Dartey Natasha Armahbea - 22125001
4. Cyril Nii Teiko Tagoe - 22241994
5. Amoako Benedict Acheampong - 22046313
6. Apeani Ann Timah - 22121034
7. Amoah Kwame Adjei - 22033203


# Project Overview

**MoodBeats** is a rule-based expert system that recommends music based on a user's emotional state and current activity. It uses SWI-Prolog for the inference engine, a Flask REST API for the backend, and a Spotify-like React interface for the frontend.

## Repository Structure

```
MoodBeats/
├── knowledge_base/          # SWI-Prolog expert system
│   ├── moodbeats.pl         # Entry point — consults all modules
│   ├── songs_kb.pl          # Song knowledge base (150+ songs)
│   ├── mood_profiles.pl     # 15 mood profiles (valence/energy/tones)
│   ├── activity_profiles.pl # 12 activity profiles (BPM ranges)
│   ├── inference_engine.pl  # Recommendation + fallback logic
│   └── explanation.pl       # Explanation generation
├── backend/                 # Flask REST API
│   ├── app.py               # API routes
│   ├── prolog_bridge.py     # Python ↔ Prolog bridge (pyswip)
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React + TypeScript UI (Spotify-style)
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── MoodSelector.tsx
│   │   │   ├── ActivitySelector.tsx
│   │   │   ├── LyricPreference.tsx
│   │   │   ├── PlaylistSize.tsx
│   │   │   ├── PlaylistResults.tsx
│   │   │   └── SongCard.tsx
│   │   └── types.ts
│   ├── package.json
│   └── .env.example
├── interface/               # CLI interface + Spotify data bridge
│   ├── moodbeats_interface.py   # Interactive terminal UI
│   ├── spotify_to_prolog.py     # Spotify → songs_kb.pl generator
│   └── requirements.txt
├── tests/
│   └── test_expert_system.py   # 39 end-to-end pytest tests
├── pytest.ini
└── README.md
```

## Team Roles
### Project Manager: Kwame Adjei Amoah

## Knowledge Engineers:
- Benedict Acheampong Amoako
- Jude Nii Klemesu Commey

## Programmers:
- Natasha Armahbea Dartey
- Cyril Nii Teiko Tagoe
- Williams Koyiri Jarawura
- Ann Timah Apeani

---

## Quick Start

### Prerequisites
- Python 3.12+
- SWI-Prolog 9.x (`swipl`)
- Node.js 18+

### 1. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Start the backend API

```bash
cd backend
cp .env.example .env  # edit if needed
python app.py
# Starts on http://localhost:5001
```

### 3. Start the React frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
# Opens on http://localhost:3000
```

### 4. Run the CLI interface (terminal only)

```bash
cd interface
pip install -r requirements.txt
python moodbeats_interface.py
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
# All 39 tests should pass
```

### Test Coverage
- Knowledge base loading and schema validation
- Song schema validation (9 required fields, value ranges)
- Inference engine: all 15 moods × activities
- Six persona test cases from the project documentation
- Flask API endpoints (all routes)

---

## Rebuilding the Song Knowledge Base from Spotify

The `songs_kb.pl` ships with 150+ curated seed songs. To rebuild it from Spotify:

```bash
# 1. Get Spotify credentials from https://developer.spotify.com
# 2. Set credentials
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"

# 3. Run the bridge
cd interface
python spotify_to_prolog.py

# 4. Restart the backend to load the new knowledge base
```

---

## API Reference

### `POST /api/recommend`

```json
{
  "mood":           "happy",
  "activity":       "working_out",
  "cognitive_load": "low",
  "playlist_size":  10
}
```

**Response:**
```json
{
  "status": "ok",
  "mood": "happy",
  "activity": "working_out",
  "cognitive_load": "low",
  "playlist": [
    {
      "id": "3n3Ppam7vgaVa1iaRUIOKE",
      "title": "Happy",
      "artist": "Pharrell Williams",
      "bpm": 160,
      "energy": 0.95,
      "instrumentalness": 0.05,
      "valence": 0.96,
      "tone": "positive",
      "lyric_complexity": "moderate"
    }
  ],
  "explanations": [...],
  "fallback": false,
  "fallback_message": null
}
```

### Cognitive Load Mapping

| Lyric Preference | Cognitive Load | Effect |
|-----------------|----------------|--------|
| Instrumental    | `high`         | Only instrumental/simple tracks |
| With Lyrics     | `low`          | Any lyric complexity |
| No Preference   | `moderate`     | All tracks accepted |

---

## Knowledge Base Design

### Mood Profiles (mood_profiles.pl)
Based on Russell's Circumplex Model of Affect (1980) and PANAS Scale (1988).

| Quadrant | Moods | Valence | Energy |
|----------|-------|---------|--------|
| Q1: +V/+E | happy, energetic, motivated, confident | High | High |
| Q2: -V/+E | angry, anxious, stressed | Low | High |
| Q3: -V/-E | sad, melancholic, tired, bored | Low | Low |
| Q4: +V/-E | calm, romantic, nostalgic, focused | High | Low |

### Inference Engine (inference_engine.pl)
- **Primary matching**: mood profile (valence + energy + tone)
- **Activity refinement**: BPM intersection with activity profile
- **Cognitive load**: determines lyric complexity filter
- **Fallback**: if no songs match mood+activity, relaxes to mood-only

