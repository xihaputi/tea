<template>
  <view class="page">
    <view class="title header">AI 智能助手</view>
    <view class="subtitle">问答与诊断助手入口</view>

    <view class="card">
      <view class="title">对话咨询</view>
      <view class="subtitle">提问茶园管理、病虫害、灌溉等问题</view>
      <view class="btn-primary" style="margin-top: 12rpx" @click="goChat">进入聊天</view>
    </view>

    <view class="card">
      <view class="title">病虫害诊断</view>
      <view class="subtitle">上传叶片照片获取诊断</view>
      <view class="btn-primary" style="margin-top: 12rpx" @click="goDisease">上传图片</view>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    goChat() {
      uni.navigateTo({ url: '/pages/chat/chat' });
    },
    goDisease() {
      uni.navigateTo({ url: '/pages/disease/disease' });
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
.header {
  padding: 24rpx 24rpx 8rpx;
}
</style>
