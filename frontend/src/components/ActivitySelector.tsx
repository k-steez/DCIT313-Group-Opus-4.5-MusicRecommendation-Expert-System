interface Props {
  selected: string
  onChange: (activity: string) => void
}

const ACTIVITIES = [
  { key: 'studying',          icon: '📚', label: 'Studying' },
  { key: 'deep_work',         icon: '💻', label: 'Deep Work' },
  { key: 'light_work',        icon: '📝', label: 'Light Work' },
  { key: 'working_out',       icon: '🏋️', label: 'Working Out' },
  { key: 'commuting',         icon: '🚌', label: 'Commuting' },
  { key: 'chores',            icon: '🧹', label: 'Chores' },
  { key: 'socializing',       icon: '🎉', label: 'Socializing' },
  { key: 'romance',           icon: '💑', label: 'Romance' },
  { key: 'grieving_venting',  icon: '💭', label: 'Venting' },
  { key: 'relaxing',          icon: '🛋️', label: 'Relaxing' },
  { key: 'sleeping',          icon: '🌙', label: 'Sleeping' },
  { key: 'meditating',        icon: '🧘', label: 'Meditating' },
]

export default function ActivitySelector({ selected, onChange }: Props) {
  return (
    <section className="section">
      <p className="section-title">Step 2</p>
      <h2 className="section-label">What are you up to?</h2>
      <p className="section-hint">Choose the activity that matches your current situation</p>
      <div className="activity-grid" role="radiogroup" aria-label="Activity selection">
        {ACTIVITIES.map(({ key, icon, label }) => (
          <button
            key={key}
            className={`activity-card${selected === key ? ' selected' : ''}`}
            onClick={() => onChange(key)}
            role="radio"
            aria-checked={selected === key}
            aria-label={label}
          >
            <span className="activity-icon">{icon}</span>
            <span className="activity-label">{label}</span>
          </button>
        ))}
      </div>
    </section>
  )
}
