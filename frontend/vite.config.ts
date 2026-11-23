import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'HARP_');
  const proxy = {
    '/api/': {
      target: process.env.HARP_API_TARGET ?? env.HARP_API_TARGET ?? 'http://127.0.0.1:8000',
      changeOrigin: true,
      rewrite: (path: string) => path.replace(/^\/api/, ''),
    },
  };

  return { plugins: [react()], server: { proxy }, preview: { proxy } };
});
