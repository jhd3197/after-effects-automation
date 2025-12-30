import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Determine if we're building for demo mode (GitHub Pages)
const isDemoMode = process.env.VITE_DEMO_MODE === 'true'
console.log('Building in demo mode:', isDemoMode)

export default defineConfig({
  // Base path for GitHub Pages (repository name)
  base: isDemoMode ? '/after-effects-automation/' : '/',

  plugins: [react()],

  // Define environment variables
  define: {
    'import.meta.env.VITE_DEMO_MODE': JSON.stringify(isDemoMode)
  },

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['framer-motion', 'react-icons']
        }
      }
    }
  },
  css: {
    modules: {
      localsConvention: 'camelCase'
    },
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler'
      }
    }
  }
})
