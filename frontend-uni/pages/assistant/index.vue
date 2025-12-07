<template>
  <view class="page-container">
    <view class="header-section">
      <view class="title-lg">AI 智能助手</view>
      <view class="text-sub" style="margin-top: 8rpx;">您的私人茶园管理专家</view>
    </view>

    <view class="service-grid">
      <!-- Chat Bot -->
      <view class="service-card" @click="goChat">
        <view class="icon-box icon-chat">
          <text class="emoji">🤖</text>
        </view>
        <view class="card-content">
          <view class="card-title">对话咨询</view>
          <view class="card-desc">解答种植、病虫害、施肥等专业问题</view>
        </view>
        <view class="action-arrow">→</view>
      </view>

      <!-- Disease Diagnosis -->
      <view class="service-card" @click="goDisease">
        <view class="icon-box icon-camera">
          <text class="emoji">📸</text>
        </view>
        <view class="card-content">
          <view class="card-title">病虫害诊断</view>
          <view class="card-desc">拍照识别病害，获取防治方案</view>
        </view>
        <view class="action-arrow">→</view>
      </view>
      
      <!-- Future Feature Placeholder -->
      <view class="service-card disabled" @click="showToast('即将上线')">
        <view class="icon-box icon-chart">
          <text class="emoji">📈</text>
        </view>
        <view class="card-content">
          <view class="card-title">产量预测</view>
          <view class="card-desc">基于历史数据预测下一季产量</view>
        </view>
        <view class="tag-coming">Coming</view>
      </view>
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
    showToast(msg) {
      uni.showToast({ title: msg, icon: 'none' });
    }
  },
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.header-section {
  padding: 24rpx 0 40rpx;
}

.service-grid {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.service-card {
  @include card-premium;
  padding: 32rpx;
  display: flex;
  align-items: center;
  position: relative;
  transition: transform 0.1s;
  
  &:active {
    transform: scale(0.99);
  }
  
  &.disabled {
    opacity: 0.7;
    background: #FAFAFA;
  }
}

.icon-box {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  font-size: 40rpx;
  
  &.icon-chat { background: #E0E7FF; color: #4F46E5; }
  &.icon-camera { background: #ECFDF5; color: #10B981; }
  &.icon-chart { background: #FFF7ED; color: #F59E0B; }
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $text-main;
  margin-bottom: 8rpx;
}

.card-desc {
  font-size: 24rpx;
  color: $text-sub;
  line-height: 1.4;
}

.action-arrow {
  color: $text-sub;
  font-size: 32rpx;
  font-weight: 300;
}

.tag-coming {
  position: absolute;
  top: 24rpx;
  right: 24rpx;
  background: #F3F4F6;
  color: $text-sub;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  font-weight: 600;
}
</style>
