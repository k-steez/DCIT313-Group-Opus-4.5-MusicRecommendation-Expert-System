import type { RecommendResponse } from '../types'
import SongCard from './SongCard'

interface Props {
  data: RecommendResponse
}

export default function PlaylistResults({ data }: Props) {
  const explanationMap = Object.fromEntries(
    (data.explanations ?? []).map((e) => [e.id, e])
  )

  return (
    <section className="section">
      <div className="results-header">
        <h2 className="results-title">
          Your Playlist
          <span className="eq-bars" aria-hidden="true">
            <span className="eq-bar" />
            <span className="eq-bar" />
            <span className="eq-bar" />
            <span className="eq-bar" />
          </span>
        </h2>
        <span className="results-count">{data.playlist.length} track{data.playlist.length !== 1 ? 's' : ''}</span>
      </div>

      {data.fallback && (
        <div className="fallback-banner" role="alert">
          <span className="fallback-icon">⚠️</span>
          <span>
            {data.fallback_message ||
              "We couldn't find an exact mood match, so we've picked the closest tracks for you."}
          </span>
        </div>
      )}

      <div className="song-list">
        {data.playlist.map((song, i) => (
          <SongCard
            key={song.id}
            song={song}
            explanation={explanationMap[song.id]}
            index={i + 1}
          />
        ))}
      </div>
    </section>
  )
}
