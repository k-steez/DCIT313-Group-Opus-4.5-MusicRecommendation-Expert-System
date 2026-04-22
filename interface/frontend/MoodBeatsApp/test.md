1. GitHub Repo Folder Structure
MoodBeats/
├── knowledge_base/
│   ├── moodbeats.pl
│   ├── inference_engine.pl
│   ├── explanation.pl
│   ├── songs_kb.pl
│   ├── mood_profiles.pl
│   └── activity_profiles.pl
├── interface/
│   └── moodbeats_interface.py
├── screenshots/
│   └── (your test case screenshots go here)
├── README.md
└── requirements.txt
requirements.txt should contain exactly one line:
pyswip

2. Exact SWI-Prolog Commands
Open a terminal, cd into the knowledge_base/ folder, then:
prolog# Launch SWI-Prolog from inside the knowledge_base/ folder
swipl

# Inside the REPL, load the top-level file
?- consult('moodbeats.pl').

# Run the test query
?- run(anxious, studying, instrumental, 5).

# To quit
?- halt.
If you want a one-liner from the terminal without entering the REPL:
bashcd knowledge_base
swipl -g "consult('moodbeats.pl'), run(anxious, studying, instrumental, 5), halt."

3. Exact Terminal Commands to Run the Python Interface
bash# 1. Make sure SWI-Prolog is installed and on your PATH
swipl --version

# 2. Install pyswip
pip install pyswip

# 3. Navigate to the interface folder
cd MoodBeats/interface

# 4. Run the interface
python moodbeats_interface.py
If you are on a system where python points to Python 2, use:
bashpython3 moodbeats_interface.py
If pyswip cannot find your SWI-Prolog shared library (common on Linux/macOS), set the path first:
bash# macOS (Homebrew)
export LIBSWIPL_PATH=$(brew --prefix)/lib/libswipl.dylib
python3 moodbeats_interface.py

# Ubuntu/Debian
export LIBSWIPL_PATH=/usr/lib/libswipl.so
python3 moodbeats_interface.py
```

---

## 4. Six Test Cases for the Report

The Thayer quadrant maps **valence** (positive/negative) against **energy** (high/low).

---

### Test Case 1 — High Energy, Positive Valence (Quadrant I)
```
Mood:           happy
Activity:       exercising
Lyric pref:     with_lyrics
Playlist limit: 5
```
**What to verify:** All returned songs should have high valence and high energy values. BPM should fall within the exercising activity profile range. Screenshot the full playlist + first explanation block.

---

### Test Case 2 — High Energy, Negative Valence (Quadrant II)
```
Mood:           angry
Activity:       gaming
Lyric pref:     with_lyrics
Playlist limit: 5
```
**What to verify:** Songs should have low valence but high energy. Tone should match the angry mood profile. Screenshot the playlist and one explanation showing tone compatibility.

---

### Test Case 3 — Low Energy, Positive Valence (Quadrant III)
```
Mood:           calm
Activity:       meditation
Lyric pref:     instrumental
Playlist limit: 5
```
**What to verify:** Songs should have high valence but low energy. BPM should be low per the meditation activity profile. Screenshot the playlist and one explanation showing BPM in range.

---

### Test Case 4 — Low Energy, Negative Valence (Quadrant IV)
```
Mood:           sad
Activity:       sleeping
Lyric pref:     no_preference
Playlist limit: 5
```
**What to verify:** Songs should have low valence and low energy. Screenshot the playlist and one explanation showing both valence and energy constraints satisfied.

---

### Test Case 5 — Cognitive Load Override (High Load)
```
Mood:           focused
Activity:       studying
Lyric pref:     instrumental
Playlist limit: 5
```
**What to verify:** The `lyric_compatible` high-cognitive-load override rule fires — only `simple` or `instrumental` tracks should appear. Screenshot the explanation block showing `Cognitive load: high` and `Compatible: yes` for lyric complexity.

---

### Test Case 6 — Fallback Triggered
```
Mood:           (choose the most obscure/niche mood in your songs_kb, e.g. fearful)
Activity:       exercising
Lyric pref:     instrumental
Playlist limit: 10
What to verify: The strict mood + activity + BPM intersection returns zero results, so safe_recommend/5 falls back to recommend_fallback/5. Screenshot the printed fallback warning message — [MoodBeats Warning] No perfect match found; playlist generated using mood profile only. — followed by the relaxed playlist.

Screenshot checklist for the report:
#TestMust show in screenshot1happy / exercisingPlaylist + explanation with valence & energy values2angry / gamingPlaylist + tone compatibility line3calm / meditationPlaylist + BPM in range line4sad / sleepingPlaylist + both valence and energy in range5focused / studyingExplanation showing cognitive load override6fearful / exercisingFallback warning message visible above playlist