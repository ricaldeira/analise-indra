import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'static/dist',
    assetsDir: 'assets',
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'frontend/src/main.js'),
        dashboard: resolve(__dirname, 'frontend/src/dashboard.js')
      },
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'frontend/src'),
      '~': resolve(__dirname, 'frontend/src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    cors: true,
    fs: {
      // Restrict file watching to only the necessary directories
      allow: ['.', './frontend', './node_modules'],
      deny: ['**/venv/**', '**/node_modules/.vite/**', '**/static/dist/**']
    }
  }
})