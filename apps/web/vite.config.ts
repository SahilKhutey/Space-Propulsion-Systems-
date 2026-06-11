import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/ws':  { target: 'ws://localhost:8000', ws: true, changeOrigin: true },
    },
  },
  define: {
    CESIUM_BASE_URL: JSON.stringify('https://cdn.jsdelivr.net/npm/cesium@1.119/Build/Cesium'),
  },
  optimizeDeps: { exclude: ['cesium'] },
})
