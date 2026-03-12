
%% within_range(+Value, +Low, +High)
%  True when Low =< Value =< High.
within_range(Value, Low, High) :-
    Value >= Low,
    Value =< High.

%% tone_compatible(+SongTone, +MoodTones)
%
%  True when the song's tone is a member of the mood's compatible
%  tone list, or when the list contains the wildcard atom 'any'.
tone_compatible(_, MoodTones) :-
    member(any, MoodTones), !.
tone_compatible(Tone, MoodTones) :-
    member(Tone, MoodTones).


%% lyric_compatible(+LyricComplexity, +CognitiveLoad, +Activity)
%
%  True when the song's lyric complexity suits the cognitive load.
%
%  Complexity atoms: simple | moderate | complex
%  Cognitive-load override rules:
%    - high:     only 'simple' lyrics are compatible.
%    - low:      'simple' and 'moderate' are compatible;
%                'complex' allowed only for leisure/meditation.
%    - moderate: all complexities are compatible.
lyric_compatible(simple, high, _).
lyric_compatible(_, high, _) :- !, fail.

lyric_compatible(simple, low, _).
lyric_compatible(moderate, low, _).
lyric_compatible(complex, low, Activity) :-
    member(Activity, [relaxing, meditating, grieving_venting, romance]).

lyric_compatible(_, moderate, _).

%% recommend(+Mood, +Activity, +CognitiveLoad, +MinBPM, +MaxBPM,
%%           +PlaylistSize, -Playlist)
%
%  Mood-first, activity-refined recommendation strategy.
%  1. Fetch the mood profile to get valence range, energy range, and tones.
%  2. Fetch the activity profile to get BPM range (intersected with caller's).
%  3. Collect all songs satisfying every constraint.
%  4. Return up to PlaylistSize tracks (as IDs).
recommend(Mood, Activity, CognitiveLoad, MinBPM, MaxBPM, PlaylistSize, Playlist) :-
    mood_profile(Mood, ValenceLow, ValenceHigh, EnergyLow, EnergyHigh, MoodTones),
    activity_profile(Activity, ActMinBPM, ActMaxBPM),
    EffMinBPM is max(MinBPM, ActMinBPM),
    EffMaxBPM is min(MaxBPM, ActMaxBPM),
    findall(SongId,
        (   song(SongId, _Title, _Artist, BPM, Energy, _Instr, Valence, Tone, LyricComplexity),
            within_range(Valence, ValenceLow, ValenceHigh),
            within_range(Energy,  EnergyLow,  EnergyHigh),
            within_range(BPM,     EffMinBPM,  EffMaxBPM),
            tone_compatible(Tone, MoodTones),
            lyric_compatible(LyricComplexity, CognitiveLoad, Activity)
        ),
        Candidates),
    generate_playlist(Candidates, PlaylistSize, Playlist).

%% recommend_fallback(+Mood, +CognitiveLoad, +PlaylistSize, -Playlist, -Message)
%
%  Relaxed fallback: ignores activity BPM constraints and uses only
%  the mood profile.  Returns a warning message alongside the playlist.
recommend_fallback(Mood, CognitiveLoad, PlaylistSize, Playlist, Message) :-
    mood_profile(Mood, ValenceLow, ValenceHigh, EnergyLow, EnergyHigh, MoodTones),
    findall(SongId,
        (   song(SongId, _Title, _Artist, _BPM, Energy, _Instr, Valence, Tone, LyricComplexity),
            within_range(Valence, ValenceLow, ValenceHigh),
            within_range(Energy,  EnergyLow,  EnergyHigh),
            tone_compatible(Tone, MoodTones),
            lyric_compatible(LyricComplexity, CognitiveLoad, general)
        ),
        Candidates),
    generate_playlist(Candidates, PlaylistSize, Playlist),
    Message = 'No perfect match found; playlist generated using mood profile only.'.

%% generate_playlist(+Candidates, +Size, -Playlist)
%
%  Takes up to Size elements from Candidates.
generate_playlist(Candidates, Size, Playlist) :-
    length(Candidates, Total),
    ( Total =< Size
    ->  Playlist = Candidates
    ;   length(Playlist, Size),
        append(Playlist, _, Candidates)
    ).

%% safe_recommend(+Mood, +Activity, +CognitiveLoad, +PlaylistSize, -Playlist)
%
%  Tries the full recommend/7 first (BPM range 0–300 as open bounds).
%  If it returns an empty playlist, falls back to recommend_fallback/5
%  and prints the fallback message.
safe_recommend(Mood, Activity, CognitiveLoad, PlaylistSize, Playlist) :-
    recommend(Mood, Activity, CognitiveLoad, 0, 300, PlaylistSize, Playlist),
    Playlist \= [],
    !.
safe_recommend(Mood, _Activity, CognitiveLoad, PlaylistSize, Playlist) :-
    recommend_fallback(Mood, CognitiveLoad, PlaylistSize, Playlist, Message),
    Playlist \= [],
    !,
    format("~n[MoodBeats Warning] ~w~n", [Message]).
safe_recommend(_Mood, _Activity, _CognitiveLoad, _PlaylistSize, []) :-
    format("~n[MoodBeats Warning] No songs available for the given parameters.~n").
