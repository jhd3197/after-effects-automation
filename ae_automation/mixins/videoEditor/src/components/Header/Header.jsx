import { useState } from 'react'
import { FaPlay, FaVideo, FaDownload, FaCircle, FaGithub, FaCopy, FaTimes } from 'react-icons/fa'
import useEditorStore from '../../store/useEditorStore'
import VideoPlayer from '../VideoPlayer/VideoPlayer'
import styles from './Header.module.scss'

function Header() {
  const { filePath, renderProject, isRendering, isDemoMode, project } = useEditorStore()
  const [showModal, setShowModal] = useState(false)
  const [showExportModal, setShowExportModal] = useState(false)
  const [outputPath, setOutputPath] = useState('output.mp4')
  const [renderStatus, setRenderStatus] = useState(null)
  const [renderedVideo, setRenderedVideo] = useState(null)
  const [copyStatus, setCopyStatus] = useState('Copy to Clipboard')

  const handleRender = async () => {
    try {
      setRenderStatus('Rendering... This may take a few minutes.')
      const result = await renderProject(outputPath)

      if (result.success) {
        setRenderStatus(`✓ Success! Output: ${result.output_path} (${result.file_size_mb} MB)`)
        setRenderedVideo(result.output_path)
        setTimeout(() => {
          setShowModal(false)
          setRenderStatus(null)
        }, 3000)
      } else {
        setRenderStatus(`✗ Error: ${result.error}`)
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || error.message
      const details = error.response?.data?.details || ''
      setRenderStatus(`✗ Error: ${errorMsg}${details ? '\n\n' + details : ''}`)
    }
  }

  const handleExportJson = () => {
    setShowExportModal(true)
    setCopyStatus('Copy to Clipboard')
  }

  const getExportData = () => {
    return JSON.stringify({
      project: project.project,
      timeline: project.timeline,
      version: "1.0"
    }, null, 2)
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(getExportData()).then(() => {
      setCopyStatus('Copied!')
      setTimeout(() => setCopyStatus('Copy to Clipboard'), 2000)
    })
  }

  const handleClosePlayer = () => {
    setRenderedVideo(null)
  }

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <FaVideo className={styles.icon} />
        <h1>After Effects Automation</h1>
        {isDemoMode && <span className={styles.demoBadge}>Demo Mode</span>}
      </div>
      <div className={styles.projectInfo}>
        <span className={styles.label}>Project:</span>
        <span className={styles.path}>{filePath || 'No project loaded'}</span>
        <div className={styles.statusIndicator} title={isDemoMode ? "Demo Mode - No Backend Connection" : "Connected"}>
          <FaCircle color={isDemoMode ? "#dc3545" : "#28a745"} size={10} />
        </div>
      </div>

      <div className={styles.actions}>
        <a
          href="https://github.com/jhd3197/after-effects-automation"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.iconButton}
          title="View on GitHub"
        >
          <FaGithub />
        </a>

        <button
          className={styles.exportButton}
          onClick={handleExportJson}
          title="Preview Project JSON"
        >
          <FaDownload />
          <span>Preview JSON</span>
        </button>

        {!isDemoMode && (
          <button
            className={styles.renderButton}
            onClick={() => setShowModal(true)}
            disabled={isRendering}
            title="Render to MP4"
          >
            <FaPlay />
            {isRendering ? 'Rendering...' : 'MP4'}
          </button>
        )}
      </div>

      {showModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2>Render Video</h2>
            <div className={styles.formGroup}>
              <label>Output Path:</label>
              <input
                type="text"
                value={outputPath}
                onChange={(e) => setOutputPath(e.target.value)}
                placeholder="output.mp4"
              />
            </div>
            {renderStatus && (
              <div className={styles.status}>{renderStatus}</div>
            )}
            <div className={styles.modalActions}>
              <button onClick={handleRender} disabled={isRendering}>
                {isRendering ? 'Rendering...' : 'Start Render'}
              </button>
              <button onClick={() => setShowModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showExportModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <div className={styles.modalHeader}>
              <h2>Export Project JSON</h2>
              <button className={styles.closeButton} onClick={() => setShowExportModal(false)}>
                <FaTimes />
              </button>
            </div>
            <div className={styles.exportContent}>
              <textarea
                readOnly
                value={getExportData()}
                className={styles.jsonTextarea}
              />
            </div>
            <div className={styles.modalActions}>
              <button onClick={handleCopy} className={styles.copyButton}>
                <FaCopy />
                {copyStatus}
              </button>
              <button onClick={() => setShowExportModal(false)}>Close</button>
            </div>
          </div>
        </div>
      )}

      {renderedVideo && (
        <VideoPlayer videoPath={renderedVideo} onClose={handleClosePlayer} />
      )}
    </header>
  )
}

export default Header
