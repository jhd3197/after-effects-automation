import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import useEditorStore from '../../store/useEditorStore'
import TimelineScene from './TimelineScene'
import TimelineRuler from './TimelineRuler'
import styles from './Timeline.module.scss'

function Timeline() {
  const { project, zoomLevel, selectedScene, setSelectedScene } = useEditorStore()
  const [scrollLeft, setScrollLeft] = useState(0)
  const timelineRef = useRef(null)

  const timeline = project.timeline || []

  // Calculate total timeline width
  const totalDuration = Math.max(
    3600, // Minimum 1 hour
    ...timeline.map((scene) => (scene.startTime || 0) + (scene.duration || 0))
  )

  const pixelsPerSecond = zoomLevel * 10
  const totalWidth = totalDuration * pixelsPerSecond

  const handleScroll = (e) => {
    setScrollLeft(e.target.scrollLeft)
  }

  const handleTimelineClick = (e) => {
    // Deselect if clicking on empty space
    if (e.target === e.currentTarget || e.target.classList.contains(styles.track)) {
      setSelectedScene(null)
    }
  }

  return (
    <div className={styles.timeline}>
      <div className={styles.header}>
        <h2>Timeline</h2>
        <div className={styles.info}>
          <span>{timeline.length} scenes</span>
          <span>{Math.floor(totalDuration / 60)}:{(totalDuration % 60).toString().padStart(2, '0')}</span>
        </div>
      </div>

      <div
        className={styles.timelineContainer}
        ref={timelineRef}
        onScroll={handleScroll}
      >
        <div className={styles.timelineContent} style={{ width: `${totalWidth}px` }}>
          <TimelineRuler
            totalDuration={totalDuration}
            pixelsPerSecond={pixelsPerSecond}
            scrollLeft={scrollLeft}
          />

          <div className={styles.tracks} onClick={handleTimelineClick}>
            <AnimatePresence mode="popLayout">
              {timeline.map((scene, index) => (
                <TimelineScene
                  key={`scene-${index}`}
                  scene={scene}
                  index={index}
                  pixelsPerSecond={pixelsPerSecond}
                  isSelected={selectedScene === index}
                  onSelect={() => setSelectedScene(index)}
                />
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Timeline
