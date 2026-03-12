import { useState } from 'react'
import type { Song, Explanation } from '../types'

interface Props {
  song: Song
  explanation?: Explanation
  index: number
}

function CompatRow({
  pass,
  label,
  detail,
}: {
  pass: boolean
  label: string
  detail: string
}) {
  return (
    <div className="why-item">
      <span className={`check-icon ${pass ? 'check-pass' : 'check-fail'}`}>
        {pass ? '✓' : '✗'}
      </span>
      <span className="why-item-text">
        <strong>{label}:</strong> {detail}
      </span>
    </div>
  )
}

function fmt(n: number, decimals = 2) {
  return n.toFixed(decimals)
}

function fmtRange(r: [number, number] | undefined) {
  if (!r) return '–'
  return `${fmt(r[0])} – ${fmt(r[1])}`
}

export default function SongCard({ song, explanation, index }: Props) {
  const [open, setOpen] = useState(false)

  return (
    <div className="song-card">
      <div
        className="song-card-main"
        onClick={() => setOpen((o) => !o)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === 'Enter' && setOpen((o) => !o)}
        aria-expanded={open}
        aria-label={`${song.title} by ${song.artist}`}
      >
        <span className="song-index">{index}</span>

        <div className="song-info">
          <div className="song-title">{song.title}</div>
          <div className="song-artist">{song.artist}</div>
        </div>

        <div className="song-meta">
          <div className="song-bars">
            <div className="bar-row">
              <span className="bar-label">E</span>
              <div className="bar-track">
                <div
                  className="bar-fill energy"
                  style={{ width: `${Math.round(song.energy * 100)}%` }}
                />
              </div>
            </div>
            <div className="bar-row">
              <span className="bar-label">V</span>
              <div className="bar-track">
                <div
                  className="bar-fill valence"
                  style={{ width: `${Math.round(song.valence * 100)}%` }}
                />
              </div>
            </div>
          </div>

          <span className="bpm-badge">{song.bpm} BPM</span>

          <button
            className={`expand-btn${open ? ' open' : ''}`}
            aria-label={open ? 'Collapse explanation' : 'Expand explanation'}
            onClick={(e) => {
              e.stopPropagation()
              setOpen((o) => !o)
            }}
          >
            ▾
          </button>
        </div>
      </div>

      {open && explanation && (
        <div className="why-panel">
          <p className="why-title">Why this song?</p>
          <div className="why-grid">
            <CompatRow
              pass={explanation.valence_in_range}
              label="Valence"
              detail={`${fmt(explanation.valence)} in [${fmtRange(explanation.mood_valence_range)}]`}
            />
            <CompatRow
              pass={explanation.energy_in_range}
              label="Energy"
              detail={`${fmt(explanation.energy)} in [${fmtRange(explanation.mood_energy_range)}]`}
            />
            <CompatRow
              pass={explanation.tone_compatible}
              label="Tone"
              detail={`${explanation.tone} ∈ {${explanation.mood_tones?.join(', ') ?? '–'}}`}
            />
            <CompatRow
              pass={explanation.bpm_in_range}
              label="BPM"
              detail={`${explanation.bpm} in [${fmtRange(explanation.activity_bpm_range)}]`}
            />
            <CompatRow
              pass={explanation.lyric_compatible}
              label="Lyrics"
              detail={explanation.lyric_complexity ?? '–'}
            />
          </div>
        </div>
      )}

      {open && !explanation && (
        <div className="why-panel">
          <p className="section-hint">No explanation available for this track.</p>
        </div>
      )}
    </div>
  )
}
