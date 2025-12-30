import { useState } from 'react'
import { FaTimes, FaPlus, FaTrash } from 'react-icons/fa'
import { motion, AnimatePresence } from 'framer-motion'
import useEditorStore from '../../store/useEditorStore'
import styles from './SceneEditor.module.scss'

function SceneEditor({ scene, index, onClose }) {
  const { updateScene, addCustomAction } = useEditorStore()
  const [formData, setFormData] = useState({ ...scene })
  const [newAction, setNewAction] = useState({
    changeType: '',
    compName: '',
    layerName: '',
    propertyName: '',
    propertyType: '',
    value: ''
  })
  const [showActionForm, setShowActionForm] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    })
  }

  const handleSave = () => {
    updateScene(index, formData)
    onClose()
  }

  const handleAddAction = () => {
    const action = { ...newAction }
    const updatedActions = [...(formData.custom_actions || []), action]
    setFormData({ ...formData, custom_actions: updatedActions })
    setNewAction({
      changeType: '',
      compName: '',
      layerName: '',
      propertyName: '',
      propertyType: '',
      value: ''
    })
    setShowActionForm(false)
  }

  const handleRemoveAction = (actionIndex) => {
    const updatedActions = formData.custom_actions.filter((_, i) => i !== actionIndex)
    setFormData({ ...formData, custom_actions: updatedActions })
  }



  return (
    <motion.div
      className={styles.overlay}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className={styles.modal}
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={styles.header}>
          <h2>Edit Scene</h2>
          <button className={styles.closeButton} onClick={onClose}>
            <FaTimes />
          </button>
        </div>

        <div className={styles.content}>
          <div className={styles.section}>
            <h3>Basic Settings</h3>
            <div className={styles.formGrid}>
              <div className={styles.formGroup}>
                <label>Scene Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Start Time (seconds)</label>
                <input
                  type="number"
                  name="startTime"
                  value={formData.startTime}
                  onChange={handleChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Duration (seconds)</label>
                <input
                  type="number"
                  name="duration"
                  value={formData.duration}
                  onChange={handleChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Template Comp</label>
                <input
                  type="text"
                  name="template_comp"
                  value={formData.template_comp}
                  onChange={handleChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    name="reverse"
                    checked={formData.reverse}
                    onChange={handleChange}
                  />
                  <span>Reverse</span>
                </label>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sectionHeader}>
              <h3>Custom Actions</h3>
              <button
                className={styles.addButton}
                onClick={() => setShowActionForm(!showActionForm)}
              >
                <FaPlus /> Add Action
              </button>
            </div>

            <AnimatePresence>
              {showActionForm && (
                <motion.div
                  className={styles.actionForm}
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                >
                  <div className={styles.formGrid}>
                    <input
                      placeholder="Change Type"
                      value={newAction.changeType}
                      onChange={(e) => setNewAction({ ...newAction, changeType: e.target.value })}
                    />
                    <input
                      placeholder="Comp Name"
                      value={newAction.compName}
                      onChange={(e) => setNewAction({ ...newAction, compName: e.target.value })}
                    />
                    <input
                      placeholder="Layer Name"
                      value={newAction.layerName}
                      onChange={(e) => setNewAction({ ...newAction, layerName: e.target.value })}
                    />
                    <input
                      placeholder="Property Name"
                      value={newAction.propertyName}
                      onChange={(e) => setNewAction({ ...newAction, propertyName: e.target.value })}
                    />
                    <input
                      placeholder="Property Type"
                      value={newAction.propertyType}
                      onChange={(e) => setNewAction({ ...newAction, propertyType: e.target.value })}
                    />
                    <input
                      placeholder="Value"
                      value={newAction.value}
                      onChange={(e) => setNewAction({ ...newAction, value: e.target.value })}
                    />
                  </div>
                  <button className={styles.saveActionButton} onClick={handleAddAction}>
                    Save Action
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            <div className={styles.actionsList}>
              {formData.custom_actions?.map((action, i) => (
                <div key={i} className={styles.actionItem}>
                  <div className={styles.actionDetails}>
                    <strong>{action.changeType}</strong>
                    <span>{action.layerName} - {action.propertyName}</span>
                  </div>
                  <button
                    className={styles.removeButton}
                    onClick={() => handleRemoveAction(i)}
                  >
                    <FaTrash />
                  </button>
                </div>
              ))}
            </div>
          </div>


        </div>

        <div className={styles.footer}>
          <button className={styles.cancelButton} onClick={onClose}>
            Cancel
          </button>
          <button className={styles.saveButton} onClick={handleSave}>
            Save Changes
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default SceneEditor
