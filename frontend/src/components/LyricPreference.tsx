interface Props {
  selected: string
  onChange: (value: string) => void
}

const OPTIONS = [
  {
    value: 'low',
    icon: '🎵',
    title: 'With Lyrics',
    desc: 'Songs with vocals & words',
  },
  {
    value: 'high',
    icon: '🎸',
    title: 'Instrumental',
    desc: 'No lyrics — pure music',
  },
  {
    value: 'moderate',
    icon: '🎧',
    title: 'No Preference',
    desc: 'Mix of both',
  },
]

export default function LyricPreference({ selected, onChange }: Props) {
  return (
    <section className="section">
      <p className="section-title">Step 3</p>
      <h2 className="section-label">Lyric preference</h2>
      <p className="section-hint">Do you want songs with lyrics or instrumental tracks?</p>
      <div className="lyric-options" role="radiogroup" aria-label="Lyric preference">
        {OPTIONS.map(({ value, icon, title, desc }) => (
          <button
            key={value}
            className={`lyric-option${selected === value ? ' selected' : ''}`}
            onClick={() => onChange(value)}
            role="radio"
            aria-checked={selected === value}
          >
            <span className="lyric-icon">{icon}</span>
            <span className="lyric-text">
              <span className="lyric-title">{title}</span>
              <span className="lyric-desc">{desc}</span>
            </span>
          </button>
        ))}
      </div>
    </section>
  )
}
