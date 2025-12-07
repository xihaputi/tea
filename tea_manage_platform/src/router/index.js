import { createRouter, createWebHistory } from "vue-router"
import Layout from "@/layout/index.vue"

// 路由配置数组
// Route configuration array
const routes = [
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: { title: "登录" }, // 页面标题 / Page title
  },
  {
    path: "/login/register",
    component: () => import("@/views/login/register.vue"),
    meta: { title: "注册账号" },
  },
  {
    path: "/login/forget",
    component: () => import("@/views/login/forget.vue"),
    meta: { title: "找回密码" },
  },
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/dashboard",
    component: Layout,
    children: [
      {
        path: "",
        component: () => import("@/views/dashboard/index.vue"),
        meta: { title: "运营总览", requiresAuth: true }, // requiresAuth: 需要登录 / Requires login
      },
    ],
  },
  {
    path: "/tea-garden",
    component: Layout,
    children: [
      {
        path: "list",
        component: () => import("@/views/tea-garden/list.vue"),
        meta: { title: "茶园列表", requiresAuth: true },
      },
      {
        path: "detail/:id",
        component: () => import("@/views/tea-garden/detail.vue"),
        meta: { title: "茶园详情", requiresAuth: true },
      },
    ],
  },
  {
    path: "/device",
    component: Layout,
    children: [
      {
        path: "list",
        component: () => import("@/views/device/list.vue"),
        meta: { title: "设备列表", requiresAuth: true },
      },
    ],
  },
  {
    path: "/rule",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/rule/index.vue"),
        meta: { title: "规则配置", requiresAuth: true },
      },
    ],
  },
  {
    path: "/alarm",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/alarm/index.vue"),
        meta: { title: "告警记录", requiresAuth: true },
      },
    ],
  },
  {
    path: "/task",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/task/index.vue"),
        meta: { title: "计划任务", requiresAuth: true },
      },
    ],
  },

  /*
  {
    path: "/rule-engine",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/rule-engine/index.vue"),
        meta: { title: "规则引擎", requiresAuth: true },
      },
    ],
  },
  */
  {
    path: "/system",
    component: Layout,
    meta: { title: "系统管理", requiresAuth: true },
    children: [
      {
        path: "user",
        component: () => import("@/views/system/user.vue"),
        meta: { title: "用户管理", requiresAuth: true },
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
]

// 创建路由实例
// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 全局前置守卫
// Global before guard
router.beforeEach((to, from, next) => {
  // 获取 Token
  // Get Token
  const token = localStorage.getItem("tea_token")

  // 如果是登录页，直接放行
  // If login page, allow
  if (to.path === "/login") {
    next()
    return
  }

  // 如果需要认证且没有 Token，跳转到登录页
  // If auth required and no token, redirect to login
  if (to.meta.requiresAuth && !token) {
    next("/login")
  } else {
    next()
  }
})

export default router
