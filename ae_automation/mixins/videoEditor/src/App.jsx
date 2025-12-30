import { useEffect } from 'react'
import useEditorStore from './store/useEditorStore'
import Header from './components/Header/Header'
import Toolbar from './components/Toolbar/Toolbar'
import ProjectPanel from './components/ProjectPanel/ProjectPanel'
import Timeline from './components/Timeline/Timeline'
import styles from './App.module.scss'

function App() {
  const { loadProject, isLoading, error } = useEditorStore()

  useEffect(() => {
    loadProject()
  }, [loadProject])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+Z for undo
      if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        e.preventDefault()
        useEditorStore.getState().undo()
      }
      // Ctrl+Shift+Z or Ctrl+Y for redo
      if ((e.ctrlKey && e.shiftKey && e.key === 'z') || (e.ctrlKey && e.key === 'y')) {
        e.preventDefault()
        useEditorStore.getState().redo()
      }
      // Delete key to delete selected scene
      if (e.key === 'Delete') {
        const selectedScene = useEditorStore.getState().selectedScene
        if (selectedScene !== null) {
          useEditorStore.getState().deleteScene(selectedScene)
          useEditorStore.getState().setSelectedScene(null)
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Loading project...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className={styles.error}>
        <h2>Error loading project</h2>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className={styles.app}>
      <Header />
      <Toolbar />
      <div className={styles.mainContent}>
        <ProjectPanel />
        <div className={styles.centerPanel}>
          <Timeline />
        </div>
      </div>
    </div>
  )
}

export default App
