<template>
  <div class="iframe-container">
    <iframe src="http://localhost:1880" frameborder="0" width="100%" height="100%"></iframe>
  </div>
</template>

<style scoped>
.iframe-container {
  width: 100%;
  height: calc(100vh - 80px); /* 减去头部高度 */
  overflow: hidden;
}
</style>
