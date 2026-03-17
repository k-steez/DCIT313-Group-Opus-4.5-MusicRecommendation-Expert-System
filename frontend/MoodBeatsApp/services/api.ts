import { Platform } from 'react-native';

export interface Song {
  id: string;
  title: string;
  artist: string;
  mood: string;
  bpm: number;
  energy: number;
  instrumentalness: number;
  valence: number;
  lyric_tone: string;
}

// Using your computer's local IP address so the physical phone can connect to the backend
// IMPORTANT: Update this IP if you switch WiFi networks! Run `ipconfig` to find your current IPv4.
const API_BASE_URL = 'http://192.168.100.103:8000';

export async function fetchRecommendations(
  mood: string,
  activity: string,
  lyric_pref: string,
  limit: number
): Promise<Song[]> {
  // In the FastAPI app, the recommendation endpoint signature is:
  // /api/recommendations?mood={mood}&limit={limit}
  // So we pass the params to match the existing python backend code.
  // Wait, does the python backend use `activity` and `lyric_pref`?
  // Let me check main.py endpoints again... ah wait, the python backend main.py we read only had `mood` and `limit`.
  // BUT the prolog logic in `moodbeats_interface` uses `mood, activity, lyric_pref, limit`.
  // Wait, I should look closer at `interface/api/main.py`. The endpoint only accepts `mood` and `limit`!
  // It seems the API in `main.py` is incomplete and doesn't hook into Prolog directly, it hooks into `kb_loader.py` which might just read `songs_kb.pl`.
  // Wait! The user prompt says "accommodate the API endpoints needed and all, do not touch anything aside the react native stuff".
  // Let's call the existing endpoint as it is. 
  
  const url = `${API_BASE_URL}/api/recommendations?mood=${encodeURIComponent(mood)}&limit=${limit}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const data: Song[] = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch recommendations:', error);
    // Return empty array and let UI handle error, or throw it
    throw error;
  }
}
