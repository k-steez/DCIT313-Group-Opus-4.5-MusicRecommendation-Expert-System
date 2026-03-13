%% ============================================================
%% MoodBeats — Activity Profiles Knowledge Base
%% activity_profiles.pl
%%
%% Activities refine the mood-filtered song pool by BPM range
%% and cognitive load. Mood always takes priority; activity
%% narrows the effective BPM window via intersection.
%%
%% Cognitive load determines lyric compatibility:
%%   high   -> instrumental forced (Perham & Vizard, 2011)
%%   medium -> user lyric preference respected
%%   low    -> user lyric preference respected
%%
%% activity_profile(
%%   Activity,
%%   MinBPM, MaxBPM,     %% Tempo range in BPM
%%   CognitiveLoad       %% high | medium | low
%% ).
%% ============================================================


%% ── Cognitive / Productive ───────────────────────────────────

activity_profile(studying,
    60,  100,   %% BPM: steady, non-distracting
    high).      %% Lyrics impair reading comprehension — forced instrumental

activity_profile(deep_work,
    55,  90,    %% BPM: slower, deeper focus
    high).      %% Same rationale as studying

activity_profile(light_work,
    80,  120,   %% BPM: slightly more energetic tolerated
    medium).    %% Lyrics acceptable — task is less cognitively demanding


%% ── Physical ─────────────────────────────────────────────────

activity_profile(working_out,
    120, 160,   %% BPM: fast, drives physical rhythm
    low).       %% Lyrics fully acceptable

activity_profile(commuting,
    90,  130,   %% BPM: moderate — alert but not intense
    low).       %% Lyrics acceptable

activity_profile(chores,
    100, 130,   %% BPM: upbeat enough to make task enjoyable
    low).       %% Lyrics acceptable


%% ── Emotional / Social ───────────────────────────────────────

activity_profile(socializing,
    100, 130,   %% BPM: lively but conversational
    medium).    %% Lyrics acceptable but should not overpower

activity_profile(romance,
    60,  100,   %% BPM: gentle, intimate
    low).       %% Lyrics fully acceptable — tone matters most

activity_profile(grieving_venting,
    50,  85,    %% BPM: slow — matches emotional weight
    low).       %% Lyrics acceptable — emotional resonance is the goal


%% ── Rest / Recovery ──────────────────────────────────────────

activity_profile(relaxing,
    60,  90,    %% BPM: slow, unwinding
    low).       %% Lyrics acceptable

activity_profile(sleeping,
    40,  70,    %% BPM: very slow — minimal stimulation
    low).       %% Lyrics acceptable but high instrumentalness preferred

activity_profile(meditating,
    40,  75,    %% BPM: very slow — non-distracting
    low).       %% Lyrics acceptable but instrumental strongly preferred
