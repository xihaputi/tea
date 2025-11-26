<template>
  <el-container class="h-screen">
    <el-aside width="240px" class="glass-aside">
      <div class="logo-area">
        <el-icon color="#13c2c2" size="24" class="mr-2"><Leaf /></el-icon>
        <span class="font-bold text-lg">Tea Brain</span>
      </div>
      <el-menu
        router
        :default-active="$route.path"
        class="border-none"
        text-color="#606266"
        active-text-color="#13c2c2"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon><span>运营总览</span>
        </el-menu-item>
        <el-menu-item index="/tea-garden/list">
          <el-icon><Collection /></el-icon><span>茶园管理</span>
        </el-menu-item>
        <el-menu-item index="/device/list">
          <el-icon><Cpu /></el-icon><span>设备管理</span>
        </el-menu-item>
        <el-menu-item index="/rule/index">
          <el-icon><Connection /></el-icon><span>规则引擎</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="glass-header">
        <div class="flex items-center text-gray-500">
          <el-icon class="mr-2"><Fold /></el-icon>
          <span>当前位置 / {{ $route.meta.title }}</span>
        </div>
        <div class="flex items-center">
          <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
          <span class="ml-2 text-sm text-gray-600">管理员</span>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.h-screen { height: 100vh; background-color: #f5f7fa; }
.glass-aside {
  background: #fff;
  border-right: 1px solid #f0f0f0;
  box-shadow: 4px 0 16px rgba(0,0,0,0.02);
  z-index: 20;
}
.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f5f5f5;
  color: #333;
}
:deep(.el-menu-item.is-active) {
  background-color: #e6fffb !important;
  border-right: 3px solid #13c2c2;
  color: #13c2c2;
  font-weight: 500;
}
.border-none { border: none; }
.glass-header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid #ebeef5;
}
.flex { display: flex; }
.items-center { align-items: center; }
.mr-2 { margin-right: 8px; }
.ml-2 { margin-left: 8px; }
.text-lg { font-size: 18px; }
.font-bold { font-weight: bold; }
</style>
