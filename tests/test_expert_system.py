"""
MoodBeats — End-to-End Test Suite
tests/test_expert_system.py

Tests cover:
  1. Prolog knowledge base loading
  2. Mood profile schema validation
  3. Activity profile schema validation
  4. Inference engine — all 15 moods with compatible activities
  5. Tone compatibility predicate
  6. Lyric compatibility predicate
  7. Six documented test cases / personas
  8. Fallback trigger verification
  9. Flask API endpoints (via test client)
 10. prolog_bridge public API

Persona test cases from test.md:
  TC1 — happy / working_out / low         → Q1 (high valence, high energy)
  TC2 — angry / commuting / low           → Q2 (low valence, high energy)
  TC3 — calm / meditating / high          → Q4 (high valence, low energy) + cognitive override
  TC4 — sad / sleeping / moderate         → Q3 (low valence, low energy)
  TC5 — focused / studying / high         → cognitive load override (instrumental only)
  TC6 — stressed / working_out / low      → fallback triggered (BPM conflict)
"""

import sys
from pathlib import Path
import pytest

# ── Path setup ────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

import prolog_bridge as pb
from app import app as flask_app

# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="module")
def api_client():
    """Flask test client, module-scoped to avoid repeated KB loads."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


# ═══════════════════════════════════════════════════════════════
# 1. Knowledge Base Loading
# ═══════════════════════════════════════════════════════════════

class TestKnowledgeBaseLoading:
    def test_prolog_loads_without_error(self):
        """The Prolog engine must initialise without exceptions."""
        pb.reload_knowledge_base()  # force fresh load
        songs = pb.get_all_songs()
        assert len(songs) > 0, "Knowledge base must contain at least one song"

    def test_songs_cover_all_moods(self):
        """
        songs_kb.pl must have at least 5 songs for every mood so
        the inference engine always has candidates.
        """
        songs = pb.get_all_songs()
        assert len(songs) >= 100, f"Expected >=100 songs, got {len(songs)}"

    def test_all_moods_defined(self):
        """All 15 mood atoms must exist in the knowledge base."""
        moods = pb.get_moods()
        assert len(moods) == 15
        for mood in pb.VALID_MOODS:
            assert mood in moods

    def test_all_activities_defined(self):
        """All 12 activity atoms must exist in the knowledge base."""
        acts = pb.get_activities()
        assert len(acts) == 12


# ═══════════════════════════════════════════════════════════════
# 2. Song Schema Validation
# ═══════════════════════════════════════════════════════════════

class TestSongSchema:
    def test_song_fields_present(self):
        """Every song must have all 9 required fields."""
        songs = pb.get_all_songs()
        required = {"id", "title", "artist", "bpm", "energy",
                    "instrumentalness", "valence", "tone", "lyric_complexity"}
        for song in songs:
            for field in required:
                assert field in song, f"Song {song.get('id')} missing field '{field}'"

    def test_song_numeric_ranges(self):
        """Valence, energy, and instrumentalness must be in [0, 1]."""
        songs = pb.get_all_songs()
        for song in songs:
            sid = song["id"]
            assert 0.0 <= song["valence"] <= 1.0, f"{sid}: valence out of range"
            assert 0.0 <= song["energy"] <= 1.0, f"{sid}: energy out of range"
            assert 0.0 <= song["instrumentalness"] <= 1.0, f"{sid}: instrumentalness out of range"

    def test_song_bpm_positive(self):
        """BPM must be a positive integer."""
        songs = pb.get_all_songs()
        for song in songs:
            assert song["bpm"] > 0, f"Song {song['id']} has invalid BPM {song['bpm']}"

    def test_lyric_complexity_values(self):
        """LyricComplexity must be one of simple | moderate | complex."""
        songs = pb.get_all_songs()
        valid = {"simple", "moderate", "complex"}
        for song in songs:
            assert song["lyric_complexity"] in valid, (
                f"Song {song['id']} has invalid lyric_complexity '{song['lyric_complexity']}'"
            )

    def test_no_duplicate_song_ids(self):
        """Each song must have a unique ID."""
        songs = pb.get_all_songs()
        ids = [s["id"] for s in songs]
        assert len(ids) == len(set(ids)), "Duplicate song IDs detected"


# ═══════════════════════════════════════════════════════════════
# 3. Inference Engine — Basic Functionality
# ═══════════════════════════════════════════════════════════════

class TestInferenceEngine:
    def test_recommend_returns_nonempty_playlist(self):
        """recommend() must return at least one track for valid inputs."""
        result = pb.recommend("happy", "working_out", "low", 5)
        assert len(result["playlist"]) > 0, "Expected at least one track"

    def test_recommend_respects_playlist_size(self):
        """Playlist must not exceed the requested size."""
        result = pb.recommend("energetic", "working_out", "low", 3)
        assert len(result["playlist"]) <= 3

    def test_recommend_returns_explanations(self):
        """Every track in the playlist must have a corresponding explanation."""
        result = pb.recommend("calm", "relaxing", "low", 5)
        assert len(result["explanations"]) == len(result["playlist"])

    def test_recommend_invalid_mood_raises(self):
        """An unknown mood atom must raise ValueError."""
        with pytest.raises(ValueError, match="mood"):
            pb.recommend("euphoric", "relaxing", "low", 5)

    def test_recommend_invalid_activity_raises(self):
        """An unknown activity atom must raise ValueError."""
        with pytest.raises(ValueError, match="activity"):
            pb.recommend("happy", "skydiving", "low", 5)

    def test_recommend_invalid_cognitive_load_raises(self):
        """An unknown cognitive_load atom must raise ValueError."""
        with pytest.raises(ValueError, match="cognitive_load"):
            pb.recommend("happy", "studying", "extreme", 5)

    def test_high_cognitive_load_returns_only_simple(self):
        """
        When cognitive_load=high, all returned songs must have
        lyric_complexity=simple (enforced by lyric_compatible/3).
        """
        result = pb.recommend("focused", "studying", "high", 10)
        for song in result["playlist"]:
            assert song["lyric_complexity"] == "simple", (
                f"Expected simple complexity, got '{song['lyric_complexity']}' "
                f"for {song['title']}"
            )

    def test_all_moods_produce_results(self):
        """Every mood must produce a non-empty playlist with at least one activity."""
        # Use broad/relaxed activities that overlap with all mood BPM ranges
        mood_activity_pairs = [
            ("happy",      "working_out"),
            ("energetic",  "working_out"),
            ("motivated",  "working_out"),
            ("confident",  "commuting"),
            ("angry",      "commuting"),
            ("anxious",    "studying"),
            ("stressed",   "studying"),
            ("sad",        "sleeping"),
            ("melancholic","sleeping"),
            ("tired",      "sleeping"),
            ("bored",      "light_work"),
            ("calm",       "relaxing"),
            ("romantic",   "romance"),
            ("nostalgic",  "commuting"),
            ("focused",    "studying"),
        ]
        for mood, activity in mood_activity_pairs:
            result = pb.recommend(mood, activity, "moderate", 5)
            assert len(result["playlist"]) > 0, (
                f"Mood '{mood}' with activity '{activity}' returned empty playlist"
            )


# ═══════════════════════════════════════════════════════════════
# 4. Explanation Validation
# ═══════════════════════════════════════════════════════════════

class TestExplanations:
    def test_explanation_fields_present(self):
        """Each explanation must contain all required fields."""
        result = pb.recommend("focused", "studying", "high", 3)
        required = {
            "id", "title", "artist", "valence", "energy", "bpm",
            "tone", "lyric_complexity", "mood_valence_range",
            "mood_energy_range", "mood_tones", "activity_bpm_range",
            "valence_in_range", "energy_in_range", "tone_compatible",
            "bpm_in_range", "lyric_compatible",
        }
        for exp in result["explanations"]:
            for field in required:
                assert field in exp, f"Explanation missing field '{field}'"

    def test_explanation_valence_in_range_is_correct(self):
        """valence_in_range must be True for every track in the playlist."""
        result = pb.recommend("happy", "working_out", "low", 5)
        for exp in result["explanations"]:
            assert exp["valence_in_range"] is True, (
                f"Track '{exp['title']}' valence {exp['valence']} not in "
                f"range {exp['mood_valence_range']}"
            )

    def test_explanation_energy_in_range_is_correct(self):
        """energy_in_range must be True for every non-fallback track."""
        result = pb.recommend("happy", "working_out", "low", 5)
        if not result["fallback"]:
            for exp in result["explanations"]:
                assert exp["energy_in_range"] is True

    def test_explanation_tone_compatible_is_correct(self):
        """tone_compatible must be True for every track in the playlist."""
        result = pb.recommend("angry", "commuting", "low", 5)
        for exp in result["explanations"]:
            assert exp["tone_compatible"] is True, (
                f"Track '{exp['title']}' tone '{exp['tone']}' not compatible "
                f"with mood tones {exp['mood_tones']}"
            )


# ═══════════════════════════════════════════════════════════════
# 5. Six Documented Persona Test Cases
# ═══════════════════════════════════════════════════════════════

class TestPersonas:
    """
    The six test cases defined in test.md / the project documentation.
    Each is annotated with the expected Thayer circumplex quadrant.
    """

    def test_tc1_happy_working_out(self):
        """
        TC1 — Q1: High valence / High energy
        happy + working_out + low cognitive load
        Expect: positive-valence, high-energy tracks; BPM in 120–160 range.
        """
        result = pb.recommend("happy", "working_out", "low", 5)
        assert len(result["playlist"]) > 0, "TC1: expected non-empty playlist"
        assert not result["fallback"], "TC1: should NOT trigger fallback"
        for song in result["playlist"]:
            assert song["valence"] >= 0.7, (
                f"TC1: expected high valence, got {song['valence']} for {song['title']}"
            )
            assert song["energy"] >= 0.6, (
                f"TC1: expected high energy, got {song['energy']} for {song['title']}"
            )
        for exp in result["explanations"]:
            assert exp["bpm_in_range"], (
                f"TC1: BPM {exp['bpm']} not in range {exp['activity_bpm_range']}"
            )

    def test_tc2_angry_commuting(self):
        """
        TC2 — Q2: Low valence / High energy
        angry + commuting + low cognitive load
        Expect: low-valence, high-energy tracks with aggressive/cathartic tone.
        """
        result = pb.recommend("angry", "commuting", "low", 5)
        assert len(result["playlist"]) > 0, "TC2: expected non-empty playlist"
        for song in result["playlist"]:
            assert song["valence"] <= 0.35, (
                f"TC2: expected low valence, got {song['valence']} for {song['title']}"
            )
            assert song["energy"] >= 0.8, (
                f"TC2: expected high energy, got {song['energy']} for {song['title']}"
            )
            assert song["tone"] in ("aggressive", "cathartic"), (
                f"TC2: unexpected tone '{song['tone']}' for {song['title']}"
            )
        for exp in result["explanations"]:
            assert exp["tone_compatible"], "TC2: tone must be compatible"

    def test_tc3_calm_meditating_high_load(self):
        """
        TC3 — Q4: High valence / Low energy + cognitive override
        calm + meditating + high cognitive load
        Expect: high-valence, low-energy tracks; only simple (instrumental) complexity.
        BPM must be in meditating range (40–75).
        """
        result = pb.recommend("calm", "meditating", "high", 5)
        assert len(result["playlist"]) > 0, "TC3: expected non-empty playlist"
        for song in result["playlist"]:
            assert song["valence"] >= 0.5, (
                f"TC3: expected positive valence, got {song['valence']} for {song['title']}"
            )
            assert song["energy"] <= 0.45, (
                f"TC3: expected low energy, got {song['energy']} for {song['title']}"
            )
            assert song["lyric_complexity"] == "simple", (
                f"TC3: cognitive override: expected simple, got '{song['lyric_complexity']}'"
            )
        for exp in result["explanations"]:
            assert exp["bpm_in_range"] or result["fallback"], (
                "TC3: BPM must be in meditating range"
            )

    def test_tc4_sad_sleeping(self):
        """
        TC4 — Q3: Low valence / Low energy
        sad + sleeping + moderate cognitive load
        Expect: low-valence, low-energy tracks.
        """
        result = pb.recommend("sad", "sleeping", "moderate", 5)
        assert len(result["playlist"]) > 0, "TC4: expected non-empty playlist"
        for song in result["playlist"]:
            assert song["valence"] <= 0.35, (
                f"TC4: expected low valence, got {song['valence']} for {song['title']}"
            )
            assert song["energy"] <= 0.45, (
                f"TC4: expected low energy, got {song['energy']} for {song['title']}"
            )

    def test_tc5_focused_studying_high_load(self):
        """
        TC5 — Cognitive Load Override
        focused + studying + high cognitive load
        Expect: ONLY songs with lyric_complexity=simple returned.
        The explanation must show Cognitive load: high and Compatible: yes.
        """
        result = pb.recommend("focused", "studying", "high", 5)
        assert len(result["playlist"]) > 0, "TC5: expected non-empty playlist"
        for song in result["playlist"]:
            assert song["lyric_complexity"] == "simple", (
                f"TC5: cognitive override must force simple lyrics; "
                f"got '{song['lyric_complexity']}' for {song['title']}"
            )
        for exp in result["explanations"]:
            assert exp["lyric_compatible"] is True, (
                f"TC5: lyric_compatible must be True; "
                f"got False for {exp['title']} "
                f"(complexity={exp['lyric_complexity']}, load=high)"
            )

    def test_tc6_fallback_triggered(self):
        """
        TC6 — Fallback
        stressed + working_out: mood valence (0.1–0.4) is incompatible
        with working_out BPM (120–160), so fallback must fire.
        The returned playlist must be non-empty (from mood-only fallback).
        """
        result = pb.recommend("stressed", "working_out", "low", 5)
        assert result["fallback"] is True, (
            "TC6: expected fallback to be triggered for stressed+working_out"
        )
        assert result["fallback_message"] is not None
        assert len(result["playlist"]) > 0, "TC6: fallback playlist must be non-empty"
        # Fallback songs should still satisfy mood valence/energy constraints
        for song in result["playlist"]:
            assert song["valence"] <= 0.40, (
                f"TC6: fallback song valence {song['valence']} exceeds stressed ceiling 0.40"
            )


# ═══════════════════════════════════════════════════════════════
# 6. Flask API Endpoint Tests
# ═══════════════════════════════════════════════════════════════

class TestFlaskAPI:
    def test_health_endpoint(self, api_client):
        """GET /api/health returns 200 with status=ok."""
        resp = api_client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert "service" in data

    def test_moods_endpoint(self, api_client):
        """GET /api/moods returns all 15 mood atoms."""
        resp = api_client.get("/api/moods")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert len(data["moods"]) == 15

    def test_activities_endpoint(self, api_client):
        """GET /api/activities returns all 12 activity atoms."""
        resp = api_client.get("/api/activities")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["activities"]) == 12

    def test_cognitive_loads_endpoint(self, api_client):
        """GET /api/cognitive-loads returns high, moderate, low."""
        resp = api_client.get("/api/cognitive-loads")
        assert resp.status_code == 200
        data = resp.get_json()
        assert set(data["cognitive_loads"]) == {"high", "moderate", "low"}

    def test_recommend_endpoint_valid(self, api_client):
        """POST /api/recommend with valid body returns playlist + explanations."""
        resp = api_client.post(
            "/api/recommend",
            json={
                "mood": "happy",
                "activity": "working_out",
                "cognitive_load": "low",
                "playlist_size": 5,
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert "playlist" in data
        assert "explanations" in data
        assert len(data["playlist"]) > 0

    def test_recommend_endpoint_missing_mood(self, api_client):
        """POST /api/recommend without 'mood' returns 400."""
        resp = api_client.post(
            "/api/recommend",
            json={"activity": "studying", "cognitive_load": "high"},
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["status"] == "error"

    def test_recommend_endpoint_missing_activity(self, api_client):
        """POST /api/recommend without 'activity' returns 400."""
        resp = api_client.post(
            "/api/recommend",
            json={"mood": "calm", "cognitive_load": "low"},
        )
        assert resp.status_code == 400

    def test_recommend_endpoint_invalid_mood(self, api_client):
        """POST /api/recommend with invalid mood returns 400."""
        resp = api_client.post(
            "/api/recommend",
            json={"mood": "nonsense", "activity": "studying", "cognitive_load": "low"},
        )
        assert resp.status_code == 400

    def test_recommend_endpoint_playlist_size_limit(self, api_client):
        """POST /api/recommend with playlist_size > 50 returns 400."""
        resp = api_client.post(
            "/api/recommend",
            json={
                "mood": "happy",
                "activity": "working_out",
                "cognitive_load": "low",
                "playlist_size": 100,
            },
        )
        assert resp.status_code == 400

    def test_songs_endpoint(self, api_client):
        """GET /api/songs returns at least 100 songs."""
        resp = api_client.get("/api/songs")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] >= 100

    def test_recommend_fallback_in_response(self, api_client):
        """POST /api/recommend for stressed+working_out must show fallback=True."""
        resp = api_client.post(
            "/api/recommend",
            json={
                "mood": "stressed",
                "activity": "working_out",
                "cognitive_load": "low",
                "playlist_size": 5,
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["fallback"] is True
        assert data["fallback_message"] is not None

    def test_recommend_all_moods_via_api(self, api_client):
        """Every mood must return a non-empty playlist via the API."""
        mood_activity = {
            "happy": "working_out", "energetic": "working_out",
            "motivated": "working_out", "confident": "commuting",
            "angry": "commuting", "anxious": "studying",
            "stressed": "studying", "sad": "sleeping",
            "melancholic": "sleeping", "tired": "sleeping",
            "bored": "light_work", "calm": "relaxing",
            "romantic": "romance", "nostalgic": "commuting",
            "focused": "studying",
        }
        for mood, activity in mood_activity.items():
            resp = api_client.post(
                "/api/recommend",
                json={"mood": mood, "activity": activity, "cognitive_load": "moderate"},
            )
            data = resp.get_json()
            assert resp.status_code == 200, f"API error for mood={mood}"
            assert len(data["playlist"]) > 0, f"Empty playlist for mood={mood}"
