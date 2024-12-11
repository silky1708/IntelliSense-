import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
})

// server: {
//   proxy: {
//     '/api': {
//       target: 'http://127.0.0.1:5000',
//       changeOrigin: true,
//       rewrite: (path) => path.replace(/^\/api/, '')
//     }
//   }
// }
// server: {
//   proxy: {
//     '/suggest': {
//         target: 'http://127.0.0.1:5000/suggest', // URL of your Flask server
//         changeOrigin: true, // Ensures the host header is updated
//         secure: false, // For development, ignore SSL certificates
//     },
// },
// },
// server: {
//   proxy: {
//     '/api': {
//       target: 'http://127.0.0.1:5000',
//       changeOrigin: true,
//       rewrite: (path) => path.replace(/^\/api/, '')
//     }
//   }
// }
