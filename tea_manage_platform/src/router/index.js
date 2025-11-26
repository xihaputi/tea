import { createRouter, createWebHistory } from "vue-router"
import Layout from "@/layout/index.vue"

const routes = [
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: { title: "登录" },
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
        meta: { title: "运营总览", requiresAuth: true },
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
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("tea_token")
  if (to.path === "/login") {
    next()
    return
  }
  if (to.meta.requiresAuth && !token) {
    next("/login")
  } else {
    next()
  }
})

export default router
