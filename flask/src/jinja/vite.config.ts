import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';

/**
 * @type {import('vite').UserConfig}
 */
export default defineConfig({
  plugins: [
    eslint()
  ],
  css: {
    preprocessorOptions: {
      scss: {}
    }
  },
  publicDir: '/',
  build: {
    rollupOptions: {
      input: [
        'front/main.ts'
      ],
      output: {
        dir: 'static',
        entryFileNames: 'index-[hash:8].js'
      }
    },
    sourcemap: true,
    outDir: 'static',
    manifest: true
  }
});
