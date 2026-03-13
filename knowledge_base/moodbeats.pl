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
print_playlist([Track|Rest], Index) :-
    format("~w. ~w~n", [Index, Track]),
    Next is Index + 1,
    print_playlist(Rest, Next).

explain_all([], _, _, _).
explain_all([Track|Rest], Mood, Activity, CognitiveLoad) :-
    explain(Track, Mood, Activity, CognitiveLoad),
    explain_all(Rest, Mood, Activity, CognitiveLoad).