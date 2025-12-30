import { useState, useEffect } from 'react'
import { FaCog, FaFile, FaChevronDown, FaChevronRight } from 'react-icons/fa'
import useEditorStore from '../../store/useEditorStore'
import styles from './ProjectPanel.module.scss'

function ProjectPanel() {
  const { project, updateProjectSettings, filePath } = useEditorStore()
  const [isExpanded, setIsExpanded] = useState(true)
  const [formData, setFormData] = useState(project.project)

  // Sync formData when project data changes from the store
  useEffect(() => {
    setFormData(project.project)
  }, [project.project])

  // Calculate resolved absolute path for display
  const getResolvedPath = () => {
    const projectFile = formData.project_file || ''
    if (!projectFile) return ''

    // If already absolute (contains : on Windows or starts with / on Unix)
    if (projectFile.includes(':') || projectFile.startsWith('/')) {
      return projectFile
    }

    // If relative, show what it will resolve to
    if (filePath) {
      // Just return filename for cleaner UI as requested
      const filename = projectFile.split(/[/\\]/).pop()
      return filename
    }

    return projectFile.split(/[/\\]/).pop()
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    const newData = { ...formData, [name]: value }
    setFormData(newData)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    updateProjectSettings(formData)
  }

  const handleBlur = () => {
    updateProjectSettings(formData)
  }

  return (
    <div className={styles.projectPanel}>
      <div className={styles.header} onClick={() => setIsExpanded(!isExpanded)}>
        <div className={styles.title}>
          <FaCog />
          <h2>Project Settings</h2>
        </div>
        {isExpanded ? <FaChevronDown /> : <FaChevronRight />}
      </div>

      {isExpanded && (
        <div className={styles.content}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGroup}>
              <label>
                <FaFile />
                Project File
              </label>
              <input
                type="text"
                name="project_file"
                value={formData.project_file || ''}
                onChange={handleChange}
                onBlur={handleBlur}
                placeholder="C:/path/to/project.aep or ./relative/path.aep"
              />
              {formData.project_file && (
                <div className={styles.pathHint} title={formData.project_file}>
                  <strong>File:</strong> {getResolvedPath()}
                </div>
              )}
            </div>

            <div className={styles.formGroup}>
              <label>Composition Name</label>
              <input
                type="text"
                name="comp_name"
                value={formData.comp_name || ''}
                onChange={handleChange}
                onBlur={handleBlur}
                placeholder="FinalComposition"
              />
              {formData.comp_name === 'FinalComposition' && (
                <div className={styles.pathHint}>
                  <strong>Note:</strong> FinalComposition requires ae_automation.aep (created by running automation). Will auto-detect if available.
                </div>
              )}
            </div>

            <div className={styles.formGroup}>
              <label>Width</label>
              <input
                type="number"
                name="width"
                value={formData.width || 1920}
                onChange={handleChange}
                onBlur={handleBlur}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Height</label>
              <input
                type="number"
                name="height"
                value={formData.height || 1080}
                onChange={handleChange}
                onBlur={handleBlur}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Frame Rate</label>
              <input
                type="number"
                name="frameRate"
                value={formData.frameRate || 30}
                onChange={handleChange}
                onBlur={handleBlur}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Duration (seconds)</label>
              <input
                type="number"
                name={formData.comp_end_time !== undefined ? "comp_end_time" : "duration"}
                value={formData.comp_end_time !== undefined ? formData.comp_end_time : (formData.duration || 60)}
                onChange={handleChange}
                onBlur={handleBlur}
              />
            </div>
          </form>

          <div className={styles.resources}>
            <h3>Resources</h3>
            <div className={styles.resourceList}>
              {project.project.resources && project.project.resources.length > 0 ? (
                project.project.resources.map((resource, index) => (
                  <div key={index} className={styles.resourceItem}>
                    <span className={styles.resourceName}>{resource.name}</span>
                    <span className={styles.resourceType}>{resource.type}</span>
                  </div>
                ))
              ) : (
                <p className={styles.empty}>No resources found</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProjectPanel
