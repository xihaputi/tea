import { createSSRApp } from 'vue';
import App from './App.vue';

export function createApp() {
  const app = createSSRApp(App);

  // Set global base URL for images
  app.config.globalProperties.$baseUrl = 'http://127.0.0.1:8000';

  return { app };
}
