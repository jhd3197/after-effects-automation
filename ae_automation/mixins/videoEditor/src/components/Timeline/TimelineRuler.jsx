import styles from './TimelineRuler.module.scss'

function TimelineRuler({ totalDuration, pixelsPerSecond }) {
  const interval = pixelsPerSecond < 20 ? 30 : pixelsPerSecond < 50 ? 15 : 5
  const marks = []

  for (let time = 0; time <= totalDuration; time += interval) {
    const position = time * pixelsPerSecond
    const minutes = Math.floor(time / 60)
    const seconds = time % 60
    const label = `${minutes}:${seconds.toString().padStart(2, '0')}`

    marks.push(
      <div
        key={time}
        className={styles.mark}
        style={{ left: `${position}px` }}
      >
        <div className={styles.tick} />
        <span className={styles.label}>{label}</span>
      </div>
    )
  }

  return (
    <div className={styles.ruler}>
      {marks}
    </div>
  )
}

export default TimelineRuler
