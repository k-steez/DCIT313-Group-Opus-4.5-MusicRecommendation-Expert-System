% knowledge_base/explanation.pl

%% explain(+Track, +Mood, +Activity, +CognitiveLoad)
%
%  Prints a full human-readable explanation for why Track was selected
%  for the given Mood, Activity, and CognitiveLoad.
explain(Track, Mood, Activity, CognitiveLoad) :-
    song(Track, Valence, Energy, BPM, Tone, LyricComplexity),
    mood_profile(Mood, ValenceLow, ValenceHigh, EnergyLow, EnergyHigh, MoodTone),
    activity_profile(Activity, ActMinBPM, ActMaxBPM),
    format("~n--- ~w ---~n", [Track]),
    format("  Mood targeted  : ~w~n", [Mood]),
    format("  Activity       : ~w~n", [Activity]),
    format("  Cognitive load : ~w~n", [CognitiveLoad]),
    format("~n  [Valence]~n"),
    format("    Song value   : ~w~n", [Valence]),
    format("    Mood range   : ~w – ~w~n", [ValenceLow, ValenceHigh]),
    explain_in_range(Valence, ValenceLow, ValenceHigh, valence),
    format("~n  [Energy]~n"),
    format("    Song value   : ~w~n", [Energy]),
    format("    Mood range   : ~w – ~w~n", [EnergyLow, EnergyHigh]),
    explain_in_range(Energy, EnergyLow, EnergyHigh, energy),
    format("~n  [Tone]~n"),
    format("    Song tone    : ~w~n", [Tone]),
    format("    Mood tone    : ~w~n", [MoodTone]),
    ( tone_compatible(Tone, MoodTone)
    ->  format("    Compatible   : yes~n")
    ;   format("    Compatible   : no~n")
    ),
    format("~n  [BPM]~n"),
    format("    Song BPM     : ~w~n", [BPM]),
    format("    Activity BPM : ~w – ~w~n", [ActMinBPM, ActMaxBPM]),
    ( within_range(BPM, ActMinBPM, ActMaxBPM)
    ->  format("    In range     : yes~n")
    ;   format("    In range     : no (fallback playlist)~n")
    ),
    format("~n  [Cognitive Load & Lyric Complexity]~n"),
    format("    Lyric complexity : ~w~n", [LyricComplexity]),
    format("    Cognitive load   : ~w~n", [CognitiveLoad]),
    ( lyric_compatible(LyricComplexity, CognitiveLoad, Activity)
    ->  format("    Compatible       : yes~n")
    ;   format("    Compatible       : no~n")
    ),
    format("~n").

%% explain_in_range(+Value, +Low, +High, +Label)
%
%  Helper that prints whether Value falls within [Low, High].
explain_in_range(Value, Low, High, Label) :-
    ( within_range(Value, Low, High)
    ->  format("    ~w in range : yes~n", [Label])
    ;   format("    ~w in range : no~n",  [Label])
    ).