import { defineConfig, UserConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'url';

const originalConfig: UserConfig = {
    root: fileURLToPath(new URL('./react-app', import.meta.url)),

    plugins: [react()],

    server: {
    port: 5173,
        open: true,
},

build: {
    outDir: fileURLToPath(new URL('./dist', import.meta.url)),
        emptyOutDir: true,
},

resolve: {
    alias: {
        '@': fileURLToPath(new URL('./react-app/src', import.meta.url)),
    },
},
};

const configWithProxy: UserConfig = {
    ...originalConfig,
    server: {
        host: true,
        port: 5173,
        open: true,
        proxy: {
            '/auth': {
                target: '[http://fastapi:8000](http://fastapi:8000)',
                changeOrigin: true,
                secure: false,
            },
        },
    },
};

export default defineConfig(configWithProxy);
