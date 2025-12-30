import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import axios from 'axios'

const API_BASE = '/api'

const SCENE_COLORS = [
  '#3498db', '#e74c3c', '#2ecc71', '#f39c12',
  '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
]

const useEditorStore = create(
  immer((set, get) => ({
    // State
    project: {
      project: {
        project_file: '',
        comp_name: '',
        resources: []
      },
      timeline: []
    },
    filePath: '',
    canUndo: false,
    canRedo: false,
    selectedScene: null,
    zoomLevel: 1,

    isLoading: false,
    error: null,
    isRendering: false,
    initialZoomSet: false,
    isDemoMode: import.meta.env.VITE_DEMO_MODE === true,

    // Actions
    loadProject: async () => {
      set({ isLoading: true, error: null })
      const isDemo = get().isDemoMode

      if (isDemo) {
        // MOCK DATA FOR DEMO MODE
        console.log("Loading Demo Project...")
        const demoProject = {
          project: {
            duration: 30,
            comp_end_time: 30,
            resources: []
          },
          timeline: [
            {
              name: 'Intro Scene',
              duration: 5,
              startTime: 0,
              template_comp: 'Intro_Template',
              uiColor: SCENE_COLORS[0]
            },
            {
              name: 'Main Content',
              duration: 15,
              startTime: 5,
              template_comp: 'Content_Template',
              uiColor: SCENE_COLORS[2]
            },
            {
              name: 'Outro Scene',
              duration: 5,
              startTime: 20,
              template_comp: 'Outro_Template',
              uiColor: SCENE_COLORS[1]
            }
          ]
        }

        set({
          project: demoProject,
          filePath: 'Demo Project.aep',
          isLoading: false,
          initialZoomSet: false
        })

        // Trigger initial zoom logic for demo
        // Use a moderate zoom level that shows context without being too zoomed in
        const projectDuration = 30
        const viewportWidth = 1200 // Typical screen width for timeline
        const displayDuration = projectDuration * 1.8 // Show 1.8x project duration
        const idealZoom = viewportWidth / displayDuration
        const clampedZoom = Math.max(0.5, Math.min(10, idealZoom))
        set({ zoomLevel: clampedZoom, initialZoomSet: true })

        return
      }

      try {
        const response = await axios.get(`${API_BASE}/project`)
        const projectData = response.data.data

        // Ensure all loaded scenes have a persistent color
        if (projectData.timeline) {
          projectData.timeline.forEach((scene, index) => {
            if (!scene.uiColor) {
              scene.uiColor = SCENE_COLORS[index % SCENE_COLORS.length]
            }
          })
        }

        // Set intelligent initial zoom based on project duration
        const state = get()
        if (!state.initialZoomSet) {
          // Check all locations for duration (comp_end_time is used in some templates)
          const projectDuration = projectData.project?.comp_end_time || projectData.project?.duration || projectData.duration || 60

          // Calculate zoom so project fits nicely with context
          // Show 1.8x project duration for comfortable viewing
          const viewportWidth = 1200 // Typical screen width for timeline
          const displayDuration = projectDuration * 1.8
          const idealZoom = viewportWidth / displayDuration
          const clampedZoom = Math.max(0.5, Math.min(10, idealZoom))

          set({
            project: projectData,
            filePath: response.data.file_path,
            isLoading: false,
            zoomLevel: clampedZoom,
            initialZoomSet: true
          })
        } else {
          set({
            project: projectData,
            filePath: response.data.file_path,
            isLoading: false
          })
        }
      } catch (error) {
        set({ error: error.message, isLoading: false })
      }
    },

    updateProject: async () => {
      const isDemo = get().isDemoMode
      if (isDemo) {
        // In demo mode, just update local state without API call
        console.log("Demo mode: Project updated locally")
        return
      }

      try {
        const { project } = get()
        const response = await axios.post(`${API_BASE}/project`, { data: project })
        set({
          canUndo: response.data.can_undo,
          canRedo: response.data.can_redo
        })
      } catch (error) {
        set({ error: error.message })
      }
    },

    undo: async () => {
      const isDemo = get().isDemoMode
      if (isDemo) {
        // Demo mode: Undo not supported
        console.log("Demo mode: Undo not available")
        return
      }

      try {
        const response = await axios.post(`${API_BASE}/undo`)
        set({
          project: response.data.data,
          canUndo: response.data.can_undo,
          canRedo: response.data.can_redo
        })
      } catch (error) {
        set({ error: error.message })
      }
    },

    redo: async () => {
      const isDemo = get().isDemoMode
      if (isDemo) {
        // Demo mode: Redo not supported
        console.log("Demo mode: Redo not available")
        return
      }

      try {
        const response = await axios.post(`${API_BASE}/redo`)
        set({
          project: response.data.data,
          canUndo: response.data.can_undo,
          canRedo: response.data.can_redo
        })
      } catch (error) {
        set({ error: error.message })
      }
    },



    renderProject: async (outputPath = 'output.mp4') => {
      const isDemo = get().isDemoMode
      if (isDemo) {
        // Demo mode: Rendering not available
        console.log("Demo mode: Rendering not available without backend")
        return { success: false, error: "Rendering not available in demo mode" }
      }

      set({ isRendering: true, error: null })
      try {
        const response = await axios.post(`${API_BASE}/render`, { output_path: outputPath })
        set({ isRendering: false })
        return response.data
      } catch (error) {
        set({ error: error.message, isRendering: false })
        throw error
      }
    },

    // Timeline actions
    addScene: () => {
      set((state) => {
        // Calculate smart duration (total / 2)
        const totalDuration = state.project.project.comp_end_time || state.project.project.duration || state.project.duration || 60
        const smartDuration = totalDuration / 2

        // Pick a random color from the palette for new scenes
        const randomColor = SCENE_COLORS[Math.floor(Math.random() * SCENE_COLORS.length)]

        const newScene = {
          name: 'New Scene',
          duration: smartDuration,
          startTime: 0,
          template_comp: '',
          reverse: false,
          custom_actions: [],
          effects: [],
          uiColor: randomColor
        }
        state.project.timeline.push(newScene)
      })
      get().updateProject()
    },

    updateScene: (index, updates) => {
      set((state) => {
        Object.assign(state.project.timeline[index], updates)
      })
      get().updateProject()
    },

    moveScene: (fromIndex, toIndex) => {
      set((state) => {
        const timeline = state.project.timeline
        if (toIndex >= 0 && toIndex < timeline.length) {
          const [movedScene] = timeline.splice(fromIndex, 1)
          timeline.splice(toIndex, 0, movedScene)
        }
      })
      get().updateProject()
    },

    deleteScene: (index) => {
      set((state) => {
        state.project.timeline.splice(index, 1)
      })
      get().updateProject()
    },

    addCustomAction: (sceneIndex, action) => {
      set((state) => {
        state.project.timeline[sceneIndex].custom_actions.push(action)
      })
      get().updateProject()
    },



    // Project settings
    updateProjectSettings: (settings) => {
      set((state) => {
        Object.assign(state.project.project, settings)
      })
      get().updateProject()
    },

    // UI state
    setSelectedScene: (index) => set({ selectedScene: index }),
    setZoomLevel: (level) => set({ zoomLevel: level }),
  }))
)

export default useEditorStore
