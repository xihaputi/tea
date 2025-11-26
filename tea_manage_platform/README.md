# Tea Manage Platform (Vue 3 + Vite + Element Plus)

前端项目部署说明，包含安装依赖、运行命令以及目录结构。

## 环境要求
- Node.js ≥ 16（建议 18+）
- npm（或 pnpm/yarn，以下以 npm 为例）

## 安装依赖
```bash
cd tea_manage_platform
npm install
```

## 运行与构建
- 开发启动（默认 http://localhost:5173 ）：
```bash
npm run dev
```
- 生产构建：
```bash
npm run build
```
- 本地预览构建产物：
```bash
npm run serve
```

## 主要目录结构
```
tea_manage_platform/
├─ index.html              # Vite 入口 HTML
├─ package.json            # 包配置与脚本
├─ vite.config.js          # Vite 配置
├─ src/
│  ├─ main.js              # 入口，挂载 App 与路由、Element Plus
│  ├─ App.vue              # 根组件（路由出口 + 动画）
│  ├─ router/
│  │  └─ index.js          # 路由配置（登录、总览、茶园、设备、规则）
│  ├─ layout/
│  │  └─ index.vue         # 布局（侧边栏 + 顶部导航 + 内容区）
│  ├─ views/
│  │  ├─ login/            # 登录页（账号/密码写死 admin/admin）
│  │  ├─ dashboard/        # 运营总览页面
│  │  ├─ tea-garden/       # 茶园管理列表/详情
│  │  ├─ device/           # 设备管理列表
│  │  └─ rule/             # 规则配置占位
│  ├─ assets/              # 静态资源
│  ├─ components/          # 公共组件（如有）
│  └─ api/                 # 接口封装（如有）
└─ public/                 # 静态公共资源
```

## 使用说明
- 默认进入登录页，账号/密码写死为 `admin/admin`，登录后跳转到 `/dashboard`。
- 路由带登录守卫：未登录访问受保护页会被重定向到 `/login`。
- 左侧导航可跳转「运营总览 / 茶园管理 / 设备管理 / 规则引擎」等页面。

## 常见问题
- 若 `npm run dev` 报错，请确认 Node 版本满足要求并已执行 `npm install`。
- 端口冲突可在启动时指定：`npm run dev -- --host --port 3001`。
