export interface Song {
  id: string;
  title: string;
  artist: string;
  bpm: number;
  energy: number;
  instrumentalness: number;
  valence: number;
  tone: string;
  lyric_complexity: string;
}

export interface Explanation {
  id: string;
  title: string;
  artist: string;
  valence: number;
  energy: number;
  bpm: number;
  tone: string;
  lyric_complexity: string;
  mood_valence_range: [number, number];
  mood_energy_range: [number, number];
  mood_tones: string[];
  activity_bpm_range: [number, number];
  valence_in_range: boolean;
  energy_in_range: boolean;
  tone_compatible: boolean;
  bpm_in_range: boolean;
  lyric_compatible: boolean;
}

export interface RecommendResponse {
  playlist: Song[];
  explanations: Explanation[];
  fallback: boolean;
  fallback_message?: string;
}

export interface RecommendRequest {
  mood: string;
  activity: string;
  cognitive_load: string;
  playlist_size: number;
}
