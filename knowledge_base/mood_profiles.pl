%% ============================================================
%% MoodBeats — Mood Profiles Knowledge Base
%% mood_profiles.pl
%%
%% Grounded in:
%%   - Russell's Circumplex Model of Affect (1980)
%%   - Thayer's Extended Circumplex (1989)
%%   - PANAS Scale — Watson et al. (1988)
%%
%% mood_profile(
%%   Mood,
%%   MinValence, MaxValence,   %% Spotify valence score (0.0–1.0)
%%   MinEnergy,  MaxEnergy,    %% Spotify energy score  (0.0–1.0)
%%   MinBPM,     MaxBPM,       %% Tempo range in BPM
%%   LyricTones                %% List of compatible lyric tone atoms
%% ).
%%
%% Valid LyricTone atoms:
%%   positive | celebratory | motivational | hype | empowering |
%%   assertive | aggressive | cathartic | soothing | neutral |
%%   melancholic | reflective | bittersweet | calm |
%%   romantic | intimate | instrumental
%% ============================================================


%% ── Q1: High Valence / High Arousal ──────────────────────────

mood_profile(happy,
    0.7,  1.0,    %% valence:  strongly positive
    0.6,  1.0,    %% energy:   high
    110,  150,    %% BPM:      upbeat, danceable
    [positive, celebratory]).

mood_profile(energetic,
    0.6,  1.0,    %% valence:  positive
    0.8,  1.0,    %% energy:   very high
    130,  170,    %% BPM:      fast
    [motivational, hype]).

mood_profile(motivated,
    0.6,  0.9,    %% valence:  positive but not purely euphoric
    0.7,  1.0,    %% energy:   high
    120,  160,    %% BPM:      driving
    [motivational, empowering]).

mood_profile(confident,
    0.65, 0.95,   %% valence:  positive
    0.65, 0.95,   %% energy:   high
    110,  150,    %% BPM:      upbeat
    [assertive, empowering]).


%% ── Q2: Low Valence / High Arousal ───────────────────────────

mood_profile(angry,
    0.0,  0.35,   %% valence:  negative
    0.8,  1.0,    %% energy:   very high
    130,  180,    %% BPM:      fast, intense
    [aggressive, cathartic]).

mood_profile(anxious,
    0.1,  0.4,    %% valence:  negative
    0.5,  0.8,    %% energy:   moderate-high (anticipatory tension)
    80,   120,    %% BPM:      moderate — prescriptive calm, not matching
    [soothing, neutral]).

mood_profile(stressed,
    0.1,  0.4,    %% valence:  negative
    0.55, 0.85,   %% energy:   slightly higher tolerance than anxious
    75,   115,    %% BPM:      moderate
    [soothing, neutral]).
    %% Note: stressed differs from anxious per PANAS —
    %% anxiety is anticipatory; stress is present-load driven.
    %% Stressed tolerates slightly more lyrical content than anxious.


%% ── Q3: Low Valence / Low Arousal ────────────────────────────

mood_profile(sad,
    0.0,  0.35,   %% valence:  strongly negative
    0.1,  0.45,   %% energy:   low
    50,   85,     %% BPM:      slow
    [melancholic, reflective]).

mood_profile(melancholic,
    0.1,  0.4,    %% valence:  negative but slightly higher floor than sad
    0.1,  0.4,    %% energy:   low
    55,   90,     %% BPM:      slow
    [reflective, bittersweet]).
    %% Note: deliberately separated from sad per Taruffi & Koelsch (2014)
    %% — users seek melancholic music for aesthetic pleasure.
    %% Higher valence floor reflects this nuance.

mood_profile(tired,
    0.2,  0.5,    %% valence:  mildly negative to neutral
    0.1,  0.35,   %% energy:   very low
    50,   80,     %% BPM:      slow
    [neutral, calm]).

mood_profile(bored,
    0.3,  0.55,   %% valence:  neutral — mood-lifting prescription
    0.2,  0.5,    %% energy:   low-moderate
    80,   120,    %% BPM:      moderate — prescriptive, not matching state
    [positive, neutral]).
    %% Note: bored sits at the Q3/Q4 border.
    %% Recommendation is prescriptive (lift mood) not descriptive (match state).


%% ── Q4: High Valence / Low Arousal ───────────────────────────

mood_profile(calm,
    0.5,  0.8,    %% valence:  positive
    0.1,  0.45,   %% energy:   low
    55,   90,     %% BPM:      slow to moderate
    [soothing, neutral]).

mood_profile(romantic,
    0.55, 0.85,   %% valence:  positive
    0.2,  0.55,   %% energy:   low-moderate
    60,   100,    %% BPM:      gentle
    [romantic, intimate]).

mood_profile(nostalgic,
    0.4,  0.75,   %% valence:  mixed — bittersweet by nature
    0.2,  0.55,   %% energy:   low-moderate
    65,   105,    %% BPM:      moderate
    [reflective, bittersweet]).

mood_profile(focused,
    0.4,  0.7,    %% valence:  neutral to mildly positive
    0.3,  0.65,   %% energy:   moderate
    60,   100,    %% BPM:      moderate — steady, non-distracting
    [neutral, instrumental]).
