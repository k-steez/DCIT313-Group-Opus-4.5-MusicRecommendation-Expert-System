:- consult('songs_kb.pl').
:- consult('mood_profiles.pl').
:- consult('activity_profiles.pl').
:- consult('inference_engine.pl').
:- consult('explanation.pl').

run(Mood, Activity, CognitiveLoad, PlaylistSize) :-
    safe_recommend(Mood, Activity, CognitiveLoad, PlaylistSize, Playlist),
    format("~n=== MoodBeats Playlist ===~n"),
    format("Mood: ~w | Activity: ~w | Cognitive Load: ~w~n~n",
           [Mood, Activity, CognitiveLoad]),
    print_playlist(Playlist, 1),
    format("~n=== Explanations ===~n"),
    explain_all(Playlist, Mood, Activity, CognitiveLoad).

print_playlist([], _).
print_playlist([TrackId|Rest], Index) :-
    ( song(TrackId, Title, Artist, _BPM, _Energy, _Instr, _Valence, _Tone, _Complexity)
    ->  format("~w. ~w — ~w~n", [Index, Title, Artist])
    ;   format("~w. ~w~n", [Index, TrackId])
    ),
    Next is Index + 1,
    print_playlist(Rest, Next).

explain_all([], _, _, _).
explain_all([Track|Rest], Mood, Activity, CognitiveLoad) :-
    explain(Track, Mood, Activity, CognitiveLoad),
    explain_all(Rest, Mood, Activity, CognitiveLoad).