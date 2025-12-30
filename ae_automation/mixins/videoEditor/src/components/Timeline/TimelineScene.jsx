import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaChevronDown, FaChevronUp, FaTrash, FaEdit, FaArrowUp, FaArrowDown } from 'react-icons/fa'
import useEditorStore from '../../store/useEditorStore'
import SceneEditor from './SceneEditor'
import styles from './TimelineScene.module.scss'

function TimelineScene({ scene, index, pixelsPerSecond, isSelected, onSelect }) {
  const { updateScene, deleteScene, moveScene, project } = useEditorStore()
  const [isExpanded, setIsExpanded] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [isResizing, setIsResizing] = useState(false)
  const [showEditor, setShowEditor] = useState(false)
  const dragStartX = useRef(0)
  const dragStartTime = useRef(0)
  const resizeStartX = useRef(0)
  const resizeStartDuration = useRef(0)

  const timelineLength = project.timeline?.length || 0

  const left = (scene.startTime || 0) * pixelsPerSecond
  const width = (scene.duration || 0) * pixelsPerSecond

  const handleMouseDown = (e) => {
    if (e.target.classList.contains(styles.resizeHandle)) return
    e.preventDefault()
    e.stopPropagation()
    onSelect()
    setIsDragging(true)
    dragStartX.current = e.clientX
    dragStartTime.current = scene.startTime || 0
  }

  const handleResizeMouseDown = (e) => {
    e.preventDefault()
    e.stopPropagation()
    onSelect()
    setIsResizing(true)
    resizeStartX.current = e.clientX
    resizeStartDuration.current = scene.duration || 0
  }

  const handleMouseMove = (e) => {
    if (isDragging) {
      const deltaX = e.clientX - dragStartX.current
      const deltaTime = deltaX / pixelsPerSecond
      const newStartTime = Math.max(0, dragStartTime.current + deltaTime)

      // Snap to grid (5 second intervals)
      const snappedTime = Math.round(newStartTime / 5) * 5

      updateScene(index, { startTime: snappedTime })
    } else if (isResizing) {
      const deltaX = e.clientX - resizeStartX.current
      const deltaDuration = deltaX / pixelsPerSecond
      const newDuration = Math.max(5, resizeStartDuration.current + deltaDuration)

      // Snap to grid
      const snappedDuration = Math.round(newDuration / 5) * 5

      updateScene(index, { duration: snappedDuration })
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
    setIsResizing(false)
  }

  const handleDoubleClick = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setShowEditor(true)
  }

  const handleDelete = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (window.confirm(`Delete scene "${scene.name}"?`)) {
      deleteScene(index)
    }
  }

  // Attach global mouse listeners when dragging or resizing
  useEffect(() => {
    if (isDragging || isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isDragging, isResizing, pixelsPerSecond])

  // Use persistent color from store, fallback to blue if missing
  const color = scene.uiColor || '#3498db'

  return (
    <div className={`${styles.sceneContainer} ${index % 2 === 0 ? styles.even : styles.odd}`}>
      <div className={styles.indexBadge}>
        {index + 1}
      </div>
      <motion.div
        className={`${styles.track} ${isExpanded ? styles.expanded : ''}`}
        layout
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        <motion.div
          className={`${styles.scene} ${isSelected ? styles.selected : ''} ${isDragging ? styles.dragging : ''}`}
          style={{
            left: `${left}px`,
            width: `${width}px`,
            backgroundColor: color,
          }}
          onMouseDown={handleMouseDown}
          onDoubleClick={handleDoubleClick}
          layout
        >
          <div className={styles.sceneHeader}>
            <div className={styles.sceneInfo}>
              <span className={styles.sceneName}>{scene.name}</span>
              <span className={styles.sceneDuration}>
                {Math.floor(scene.duration)}s
              </span>
            </div>
            <div className={styles.sceneActions}>
              <button
                className={styles.actionButton}
                onClick={() => setIsExpanded(!isExpanded)}
                title="Toggle details"
              >
                {isExpanded ? <FaChevronUp /> : <FaChevronDown />}
              </button>
              <button
                className={styles.actionButton}
                onClick={() => moveScene(index, index - 1)}
                disabled={index === 0}
                title="Move Up"
              >
                <FaArrowUp />
              </button>
              <button
                className={styles.actionButton}
                onClick={() => moveScene(index, index + 1)}
                disabled={index === timelineLength - 1}
                title="Move Down"
              >
                <FaArrowDown />
              </button>
              <button
                className={styles.actionButton}
                onClick={() => setShowEditor(true)}
                title="Edit scene"
              >
                <FaEdit />
              </button>
              <button
                className={`${styles.actionButton} ${styles.delete}`}
                onClick={handleDelete}
                title="Delete scene"
              >
                <FaTrash />
              </button>
            </div>
          </div>

          {isExpanded && (
            <div className={styles.sceneDetails}>
              <div className={styles.detailItem}>
                <strong>Template:</strong> {scene.template_comp || 'None'}
              </div>
              <div className={styles.detailItem}>
                <strong>Start:</strong> {scene.startTime}s
              </div>
              <div className={styles.detailItem}>
                <strong>Effects:</strong> {scene.effects?.length || 0}
              </div>
              <div className={styles.detailItem}>
                <strong>Actions:</strong> {scene.custom_actions?.length || 0}
              </div>
            </div>
          )}

          <div
            className={`${styles.resizeHandle} ${styles.right}`}
            onMouseDown={handleResizeMouseDown}
          />
        </motion.div>
      </motion.div>

      {showEditor && (
        <SceneEditor
          scene={scene}
          index={index}
          onClose={() => setShowEditor(false)}
        />
      )}
      {showEditor && (
        <SceneEditor
          scene={scene}
          index={index}
          onClose={() => setShowEditor(false)}
        />
      )}
    </div>
  )
}

export default TimelineScene
