
%% within_range(+Value, +Low, +High)
%  True when Low =< Value =< High.
within_range(Value, Low, High) :-
    Value >= Low,
    Value =< High.

%% tone_compatible(+SongTone, +MoodTone)
%
%  True when the song's tone is compatible with the mood's required tone.
%  A mood tone of 'any' matches all song tones.
tone_compatible(_, any).
tone_compatible(Tone, Tone).


%  True when the song's lyric complexity suits the cognitive load and activity.
%
%  Cognitive-load override rules (applied before general rules):
%    - High cognitive load: only 'simple' lyrics are compatible.
%    - Low cognitive load: 'simple' and 'moderate' are compatible;
%      'complex' is allowed only during 'leisure' or 'meditation'.
%    - Moderate cognitive load (default): all complexities are compatible.
lyric_compatible(simple, high, _).
lyric_compatible(_, high, _) :- !, fail.

lyric_compatible(simple, low, _).
lyric_compatible(moderate, low, _).
lyric_compatible(complex, low, Activity) :-
    member(Activity, [leisure, meditation]).

lyric_compatible(_, moderate, _).

%% recommend(+Mood, +Activity, +CognitiveLoad, +MinBPM, +MaxBPM,
%%           +PlaylistSize, -Playlist)
%
%  Mood-first, activity-refined recommendation strategy.
%  1. Fetch the mood profile to get valence range, energy range, and tone.
%  2. Fetch the activity profile to get BPM range (intersected with caller's).
%  3. Collect all songs satisfying every constraint.
%  4. Return up to PlaylistSize tracks.
recommend(Mood, Activity, CognitiveLoad, MinBPM, MaxBPM, PlaylistSize, Playlist) :-
    mood_profile(Mood, ValenceLow, ValenceHigh, EnergyLow, EnergyHigh, MoodTone),
    activity_profile(Activity, ActMinBPM, ActMaxBPM),
    EffMinBPM is max(MinBPM, ActMinBPM),
    EffMaxBPM is min(MaxBPM, ActMaxBPM),
    findall(Song,
        (   song(Song, Valence, Energy, BPM, Tone, LyricComplexity),
            within_range(Valence, ValenceLow, ValenceHigh),
            within_range(Energy,  EnergyLow,  EnergyHigh),
            within_range(BPM,     EffMinBPM,  EffMaxBPM),
            tone_compatible(Tone, MoodTone),
            lyric_compatible(LyricComplexity, CognitiveLoad, Activity)
        ),
        Candidates),
    generate_playlist(Candidates, PlaylistSize, Playlist).

%% recommend_fallback(+Mood, +CognitiveLoad, +PlaylistSize, -Playlist, -Message)
%
%  Relaxed fallback: ignores activity BPM constraints and uses only
%  the mood profile.  Returns a warning message alongside the playlist.
recommend_fallback(Mood, CognitiveLoad, PlaylistSize, Playlist, Message) :-
    mood_profile(Mood, ValenceLow, ValenceHigh, EnergyLow, EnergyHigh, MoodTone),
    findall(Song,
        (   song(Song, Valence, Energy, _BPM, Tone, LyricComplexity),
            within_range(Valence, ValenceLow, ValenceHigh),
            within_range(Energy,  EnergyLow,  EnergyHigh),
            tone_compatible(Tone, MoodTone),
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