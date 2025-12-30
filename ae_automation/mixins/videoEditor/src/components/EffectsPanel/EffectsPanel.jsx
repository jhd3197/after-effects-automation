import { useState } from 'react'
import { FaMagic, FaChevronDown, FaChevronRight, FaPlus } from 'react-icons/fa'
import useEditorStore from '../../store/useEditorStore'
import styles from './EffectsPanel.module.scss'

function EffectsPanel() {
  const { effects, selectedScene, addEffectToScene } = useEditorStore()
  const [expandedSections, setExpandedSections] = useState({
    transitions: true,
    effects: true
  })

  const toggleSection = (section) => {
    setExpandedSections({
      ...expandedSections,
      [section]: !expandedSections[section]
    })
  }

  const handleAddEffect = (effect) => {
    if (selectedScene !== null) {
      addEffectToScene(selectedScene, effect)
    } else {
      alert('Please select a scene first')
    }
  }

  return (
    <div className={styles.effectsPanel}>
      <div className={styles.header}>
        <FaMagic />
        <h2>Effects & Transitions</h2>
      </div>

      {selectedScene === null && (
        <div className={styles.notice}>
          Select a scene to add effects
        </div>
      )}

      <div className={styles.content}>
        <div className={styles.section}>
          <div
            className={styles.sectionHeader}
            onClick={() => toggleSection('transitions')}
          >
            <div className={styles.title}>
              {expandedSections.transitions ? <FaChevronDown /> : <FaChevronRight />}
              <h3>Transitions</h3>
            </div>
            <span className={styles.count}>{effects.transitions.length}</span>
          </div>

          {expandedSections.transitions && (
            <div className={styles.effectsList}>
              {effects.transitions.map((transition) => (
                <div key={transition.id} className={styles.effectItem}>
                  <div className={styles.effectInfo}>
                    <h4>{transition.name}</h4>
                    <p>{transition.description}</p>
                  </div>
                  <button
                    className={styles.addButton}
                    onClick={() => handleAddEffect(transition)}
                    disabled={selectedScene === null}
                  >
                    <FaPlus />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div
            className={styles.sectionHeader}
            onClick={() => toggleSection('effects')}
          >
            <div className={styles.title}>
              {expandedSections.effects ? <FaChevronDown /> : <FaChevronRight />}
              <h3>Effects</h3>
            </div>
            <span className={styles.count}>{effects.effects.length}</span>
          </div>

          {expandedSections.effects && (
            <div className={styles.effectsList}>
              {effects.effects.map((effect) => (
                <div key={effect.id} className={styles.effectItem}>
                  <div className={styles.effectInfo}>
                    <h4>{effect.name}</h4>
                    <p>{effect.description}</p>
                  </div>
                  <button
                    className={styles.addButton}
                    onClick={() => handleAddEffect(effect)}
                    disabled={selectedScene === null}
                  >
                    <FaPlus />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default EffectsPanel
