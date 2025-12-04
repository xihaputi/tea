import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import "element-plus/theme-chalk/dark/css-vars.css"
import * as ElementPlusIconsVue from "@element-plus/icons-vue"

// 创建 Vue 应用实例
// Create Vue application instance
const app = createApp(App)

// 注册所有 Element Plus 图标
// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用路由
// Use router
app.use(router)
// 使用 Element Plus UI 库
// Use Element Plus UI library
app.use(ElementPlus)
// 挂载应用到 DOM
// Mount application to DOM
app.mount("#app")
