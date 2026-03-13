import { create } from 'zustand';
import { Song } from '../services/api';

interface MoodBeatsState {
  mood: string | null;
  activity: string | null;
  lyricPreference: string;
  playlistLength: number;
  playlist: Song[];
  setMood: (mood: string) => void;
  setActivity: (activity: string) => void;
  setPreferences: (lyricPref: string, length: number) => void;
  setPlaylist: (playlist: Song[]) => void;
  reset: () => void;
}

export const useStore = create<MoodBeatsState>((set) => ({
  mood: 'happy', // Default from home.tsx
  activity: 'studying', // Default from activitySelection.tsx
  lyricPreference: 'with_lyrics',
  playlistLength: 10,
  playlist: [],
  setMood: (mood) => set({ mood }),
  setActivity: (activity) => set({ activity }),
  setPreferences: (lyricPreference, playlistLength) => set({ lyricPreference, playlistLength }),
  setPlaylist: (playlist) => set({ playlist }),
  reset: () => set({
    mood: 'happy',
    activity: 'studying',
    lyricPreference: 'with_lyrics',
    playlistLength: 10,
    playlist: []
  }),
}));
