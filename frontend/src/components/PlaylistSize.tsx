interface Props {
  value: number
  onChange: (value: number) => void
}

export default function PlaylistSize({ value, onChange }: Props) {
  return (
    <section className="section">
      <p className="section-title">Step 4</p>
      <h2 className="section-label">Playlist size</h2>
      <p className="section-hint">How many tracks do you want?</p>
      <div className="slider-container">
        <div className="slider-value-row">
          <div className="slider-value">
            <span className="slider-number">{value}</span>
            <span className="slider-unit">song{value !== 1 ? 's' : ''}</span>
          </div>
          <span className="slider-range">1 – 20</span>
        </div>
        <input
          type="range"
          min={1}
          max={20}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          aria-label="Playlist size"
          aria-valuemin={1}
          aria-valuemax={20}
          aria-valuenow={value}
          style={{
            background: `linear-gradient(to right, var(--accent) 0%, var(--accent) ${((value - 1) / 19) * 100}%, var(--bg-highlight) ${((value - 1) / 19) * 100}%, var(--bg-highlight) 100%)`,
          }}
        />
      </div>
    </section>
  )
}
