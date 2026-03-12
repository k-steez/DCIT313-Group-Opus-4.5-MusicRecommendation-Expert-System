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
%%   MoodTones                 %% List of compatible lyric tone atoms
%% ).
%%
%% BPM constraints are fully delegated to activity_profiles.pl.
%% Mood profiles govern the emotional/acoustic signature only.
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
    [positive, celebratory]).

mood_profile(energetic,
    0.6,  1.0,    %% valence:  positive
    0.8,  1.0,    %% energy:   very high
    [motivational, hype]).

mood_profile(motivated,
    0.6,  0.9,    %% valence:  positive but not purely euphoric
    0.7,  1.0,    %% energy:   high
    [motivational, empowering]).

mood_profile(confident,
    0.65, 0.95,   %% valence:  positive
    0.65, 0.95,   %% energy:   high
    [assertive, empowering]).


%% ── Q2: Low Valence / High Arousal ───────────────────────────

mood_profile(angry,
    0.0,  0.35,   %% valence:  negative
    0.8,  1.0,    %% energy:   very high
    [aggressive, cathartic]).

mood_profile(anxious,
    0.1,  0.4,    %% valence:  negative
    0.5,  0.8,    %% energy:   moderate-high (anticipatory tension)
    [soothing, neutral]).

mood_profile(stressed,
    0.1,  0.4,    %% valence:  negative
    0.55, 0.85,   %% energy:   slightly higher tolerance than anxious
    [soothing, neutral]).
    %% Note: stressed differs from anxious per PANAS —
    %% anxiety is anticipatory; stress is present-load driven.


%% ── Q3: Low Valence / Low Arousal ────────────────────────────

mood_profile(sad,
    0.0,  0.35,   %% valence:  strongly negative
    0.1,  0.45,   %% energy:   low
    [melancholic, reflective]).

mood_profile(melancholic,
    0.1,  0.4,    %% valence:  negative but slightly higher floor than sad
    0.1,  0.4,    %% energy:   low
    [reflective, bittersweet]).
    %% Note: deliberately separated from sad per Taruffi & Koelsch (2014)
    %% — users seek melancholic music for aesthetic pleasure.

mood_profile(tired,
    0.2,  0.5,    %% valence:  mildly negative to neutral
    0.1,  0.35,   %% energy:   very low
    [neutral, calm]).

mood_profile(bored,
    0.3,  0.55,   %% valence:  neutral — mood-lifting prescription
    0.2,  0.5,    %% energy:   low-moderate
    [positive, neutral]).
    %% Note: prescriptive (lift mood), not descriptive (match state).


%% ── Q4: High Valence / Low Arousal ───────────────────────────

mood_profile(calm,
    0.5,  0.8,    %% valence:  positive
    0.1,  0.45,   %% energy:   low
    [soothing, neutral]).

mood_profile(romantic,
    0.55, 0.85,   %% valence:  positive
    0.2,  0.55,   %% energy:   low-moderate
    [romantic, intimate]).

mood_profile(nostalgic,
    0.4,  0.75,   %% valence:  mixed — bittersweet by nature
    0.2,  0.55,   %% energy:   low-moderate
    [reflective, bittersweet]).

mood_profile(focused,
    0.4,  0.7,    %% valence:  neutral to mildly positive
    0.3,  0.65,   %% energy:   moderate
    [neutral, instrumental]).
