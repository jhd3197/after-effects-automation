import { FaUndo, FaRedo, FaPlus, FaSearchPlus, FaSearchMinus } from 'react-icons/fa'
import useEditorStore from '../../store/useEditorStore'
import styles from './Toolbar.module.scss'

function Toolbar() {
  const { canUndo, canRedo, undo, redo, addScene, zoomLevel, setZoomLevel } = useEditorStore()

  const handleZoomIn = () => {
    if (zoomLevel < 10) {
      setZoomLevel(Math.min(10, zoomLevel + 0.5))
    }
  }

  const handleZoomOut = () => {
    if (zoomLevel > 0.1) {
      setZoomLevel(Math.max(0.1, zoomLevel - 0.5))
    }
  }

  // Calculate pixels per second for display
  const pixelsPerSecond = zoomLevel * 10
  const secondsVisible = Math.floor(1000 / pixelsPerSecond) // Approximate seconds visible in 1000px

  return (
    <div className={styles.toolbar}>
      <div className={styles.group}>
        <button
          onClick={undo}
          disabled={!canUndo}
          title="Undo (Ctrl+Z)"
          className={styles.toolButton}
        >
          <FaUndo />
          <span>Undo</span>
        </button>
        <button
          onClick={redo}
          disabled={!canRedo}
          title="Redo (Ctrl+Y)"
          className={styles.toolButton}
        >
          <FaRedo />
          <span>Redo</span>
        </button>
      </div>

      <div className={styles.separator}></div>

      <div className={styles.group}>
        <button
          onClick={addScene}
          className={`${styles.toolButton} ${styles.primary}`}
          title="Add Scene"
        >
          <FaPlus />
          <span>Add Scene</span>
        </button>
      </div>

      <div className={styles.separator}></div>

      <div className={styles.group}>
        <button
          onClick={handleZoomOut}
          disabled={zoomLevel <= 0.1}
          className={styles.toolButton}
          title="Zoom Out"
        >
          <FaSearchMinus />
        </button>
        <span className={styles.zoomLevel} title={`${pixelsPerSecond.toFixed(1)} pixels/sec`}>
          {secondsVisible}s
        </span>
        <button
          onClick={handleZoomIn}
          disabled={zoomLevel >= 10}
          className={styles.toolButton}
          title="Zoom In"
        >
          <FaSearchPlus />
        </button>
        <input
          type="range"
          min="0.1"
          max="10"
          step="0.1"
          value={zoomLevel}
          onChange={(e) => setZoomLevel(parseFloat(e.target.value))}
          className={styles.zoomSlider}
          title="Zoom level"
        />
      </div>
    </div>
  )
}

export default Toolbar
