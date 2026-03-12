interface Props {
  selected: string
  onChange: (mood: string) => void
}

const MOODS = [
  { key: 'happy',      emoji: '😊', label: 'Happy' },
  { key: 'energetic',  emoji: '⚡', label: 'Energetic' },
  { key: 'motivated',  emoji: '💪', label: 'Motivated' },
  { key: 'confident',  emoji: '😎', label: 'Confident' },
  { key: 'angry',      emoji: '😤', label: 'Angry' },
  { key: 'anxious',    emoji: '😰', label: 'Anxious' },
  { key: 'stressed',   emoji: '😫', label: 'Stressed' },
  { key: 'sad',        emoji: '😢', label: 'Sad' },
  { key: 'melancholic',emoji: '🌧', label: 'Melancholic' },
  { key: 'tired',      emoji: '😴', label: 'Tired' },
  { key: 'bored',      emoji: '😑', label: 'Bored' },
  { key: 'calm',       emoji: '😌', label: 'Calm' },
  { key: 'romantic',   emoji: '🥰', label: 'Romantic' },
  { key: 'nostalgic',  emoji: '🌅', label: 'Nostalgic' },
  { key: 'focused',    emoji: '🎯', label: 'Focused' },
]

export default function MoodSelector({ selected, onChange }: Props) {
  return (
    <section className="section">
      <p className="section-title">Step 1</p>
      <h2 className="section-label">How are you feeling?</h2>
      <p className="section-hint">Pick the mood that best describes you right now</p>
      <div className="mood-grid" role="radiogroup" aria-label="Mood selection">
        {MOODS.map(({ key, emoji, label }) => (
          <button
            key={key}
            className={`mood-card${selected === key ? ' selected' : ''}`}
            onClick={() => onChange(key)}
            role="radio"
            aria-checked={selected === key}
            aria-label={label}
          >
            <span className="mood-emoji">{emoji}</span>
            <span className="mood-label">{label}</span>
          </button>
        ))}
      </div>
    </section>
  )
}
