import { useState } from 'react'
import Header from './components/Header'
import MoodSelector from './components/MoodSelector'
import ActivitySelector from './components/ActivitySelector'
import LyricPreference from './components/LyricPreference'
import PlaylistSize from './components/PlaylistSize'
import PlaylistResults from './components/PlaylistResults'
import type { RecommendResponse } from './types'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5001'

type Status = 'idle' | 'loading' | 'success' | 'error'

export default function App() {
  const [mood, setMood] = useState('')
  const [activity, setActivity] = useState('')
  const [cognitiveLoad, setCognitiveLoad] = useState('moderate')
  const [playlistSize, setPlaylistSize] = useState(10)
  const [status, setStatus] = useState<Status>('idle')
  const [result, setResult] = useState<RecommendResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState('')

  const canSubmit = mood !== '' && activity !== '' && status !== 'loading'

  async function handleSubmit() {
    if (!canSubmit) return
    setStatus('loading')
    setErrorMsg('')
    setResult(null)

    try {
      const res = await fetch(`${API_URL}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mood,
          activity,
          cognitive_load: cognitiveLoad,
          playlist_size: playlistSize,
        }),
      })

      if (!res.ok) {
        const body = await res.text()
        throw new Error(body || `Server error ${res.status}`)
      }

      const data: RecommendResponse = await res.json()
      setResult(data)
      setStatus('success')

      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : 'Something went wrong. Is the backend running?')
      setStatus('error')
    }
  }

  return (
    <div className="app">
      <Header />

      <main className="main">
        <div className="container">
          <MoodSelector selected={mood} onChange={setMood} />

          <div className="divider" />

          <ActivitySelector selected={activity} onChange={setActivity} />

          <div className="divider" />

          <LyricPreference selected={cognitiveLoad} onChange={setCognitiveLoad} />

          <div className="divider" />

          <PlaylistSize value={playlistSize} onChange={setPlaylistSize} />

          <div className="divider" />

          {/* Validation hints */}
          {(!mood || !activity) && (
            <p className="section-hint" style={{ marginBottom: '16px' }}>
              {!mood && !activity
                ? '👆 Select a mood and activity to get started'
                : !mood
                ? '👆 Select a mood to continue'
                : '👆 Select an activity to continue'}
            </p>
          )}

          <button
            className="cta-button"
            onClick={handleSubmit}
            disabled={!canSubmit}
            aria-label="Get my playlist"
          >
            <span className="cta-button-icon">🎵</span>
            {status === 'loading' ? 'Building your playlist…' : 'Get My Playlist'}
          </button>

          {/* Loading */}
          {status === 'loading' && (
            <div className="loading-wrapper" aria-live="polite" aria-busy="true">
              <div className="spinner" />
              <p className="loading-text">Curating the perfect tracks for your mood…</p>
            </div>
          )}

          {/* Error */}
          {status === 'error' && (
            <div className="error-banner" role="alert">
              <span className="error-icon">⚠️</span>
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Results */}
          {status === 'success' && result && (
            <>
              <div className="divider" id="results" />
              <PlaylistResults data={result} />
            </>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          MoodBeats · DCIT313 Expert Systems Project · Built with React + Flask
        </div>
      </footer>
    </div>
  )
}
