import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from "@element-plus/icons-vue"
import permission from './utils/permission'

// 创建 Vue 应用实例
// Create Vue application instance
const app = createApp(App)

// 注册所有 Element Plus 图标
// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.directive('permission', permission)

// 使用路由
// Use router
app.use(router)
// 使用 Element Plus UI 库
// Use Element Plus UI library
app.use(ElementPlus)
// 挂载应用到 DOM
// Mount application to DOM
app.mount("#app")
