%% ============================================================
%% MoodBeats — Activity Profiles Knowledge Base
%% activity_profiles.pl
%%
%% Activities refine the mood-filtered song pool by BPM range.
%% Mood always takes priority; activity narrows the effective
%% BPM window via intersection with mood profile energy/valence.
%%
%% Cognitive load is provided by the user at query time and
%% determines lyric compatibility (see inference_engine.pl):
%%   high   -> only simple/instrumental lyrics (Perham & Vizard, 2011)
%%   moderate -> user lyric preference respected
%%   low    -> user lyric preference respected
%%
%% activity_profile(
%%   Activity,
%%   MinBPM, MaxBPM     %% Tempo range in BPM
%% ).
%% ============================================================


%% ── Cognitive / Productive ───────────────────────────────────

activity_profile(studying,
    60,  100).   %% BPM: steady, non-distracting

activity_profile(deep_work,
    55,  90).    %% BPM: slower, deeper focus

activity_profile(light_work,
    80,  120).   %% BPM: slightly more energetic tolerated


%% ── Physical ─────────────────────────────────────────────────

activity_profile(working_out,
    120, 160).   %% BPM: fast, drives physical rhythm

activity_profile(commuting,
    90,  130).   %% BPM: moderate — alert but not intense

activity_profile(chores,
    100, 130).   %% BPM: upbeat enough to make task enjoyable


%% ── Emotional / Social ───────────────────────────────────────

activity_profile(socializing,
    100, 130).   %% BPM: lively but conversational

activity_profile(romance,
    60,  100).   %% BPM: gentle, intimate

activity_profile(grieving_venting,
    50,  85).    %% BPM: slow — matches emotional weight


%% ── Rest / Recovery ──────────────────────────────────────────

activity_profile(relaxing,
    60,  90).    %% BPM: slow, unwinding

activity_profile(sleeping,
    40,  70).    %% BPM: very slow — minimal stimulation

activity_profile(meditating,
    40,  75).    %% BPM: very slow — non-distracting
