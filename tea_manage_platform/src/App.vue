<template>
  <router-view v-slot="{ Component }">
    <!-- 页面切换过渡动画 -->
    <!-- Page transition animation -->
    <transition name="fade-slide" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
/* 全局基础重置 */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa; /* 极淡的灰背景，护眼且现代 */
  color: #2c3e50;
  -webkit-font-smoothing: antialiased;
}

/* 页面切换动画：淡入并轻微上浮 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 4px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
</style>