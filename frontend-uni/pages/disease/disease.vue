<template>
  <view class="page-container">
    <view class="header-box">
      <view class="title-lg">病虫害智能诊断</view>
      <view class="text-sub" style="margin-top: 8rpx;">拍摄茶树叶片，AI 快速识别病害类型</view>
    </view>

    <!-- Upload Area -->
    <view class="upload-card" @click="chooseImage">
      <block v-if="filePath">
        <image :src="filePath" mode="aspectFit" class="preview-img"></image>
        <view class="re-upload-btn">重新拍照</view>
      </block>
      <block v-else>
        <view class="upload-placeholder">
          <text class="camera-icon">📸</text>
          <text class="upload-text">点击上传 / 拍摄照片</text>
          <text class="upload-hint">请确保光线充足，病灶清晰</text>
        </view>
      </block>
    </view>
    
    <!-- Upload Button -->
    <button v-if="filePath && !uploading && !result" class="btn-primary full-btn" @click.stop="upload">开始诊断</button>
    <button v-if="uploading" class="btn-primary full-btn disabled" disabled>正在分析...</button>

    <!-- Result Card -->
    <view v-if="result" class="card result-card">
      <view class="result-header">
        <text class="result-title">诊断结果</text>
        <view class="confidence-tag">可信度 {{ (result.confidence * 100).toFixed(1) }}%</view>
      </view>
      
      <view class="result-row">
        <text class="label">病害类型：</text>
        <text class="value highlight">{{ result.disease_type }}</text>
      </view>
      
      <view class="divider"></view>
      
      <view class="advice-section">
        <text class="label">防治建议：</text>
        <text class="advice-text">{{ result.advice }}</text>
      </view>
    </view>
    
    <view v-if="error" class="error-msg">{{ error }}</view>
  </view>
</template>

<script>
import { detectDisease } from '@/api/disease.js';

export default {
  data() {
    return {
      filePath: '',
      result: null,
      uploading: false,
      error: '',
    };
  },
  methods: {
    chooseImage() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        success: (res) => {
          this.filePath = res.tempFilePaths[0];
          this.result = null; // Clear previous result
          this.error = '';
        },
        fail: () => {
          // User cancelled
        },
      });
    },
    async upload() {
      if (!this.filePath) return;
      this.uploading = true;
      this.error = '';
      try {
        const res = await detectDisease(this.filePath);
        this.result = res;
      } catch (e) {
        this.error = '识别失败，请检查网络或重试';
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page-container {
  padding: 24rpx;
}

.header-box {
  margin-bottom: 40rpx;
}

.upload-card {
  background: #fff;
  border: 4rpx dashed #D1D5DB;
  border-radius: 24rpx;
  height: 400rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
  position: relative;
  overflow: hidden;
  
  &:active {
    background: #F9FAFB;
  }
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.camera-icon {
  font-size: 80rpx;
  margin-bottom: 16rpx;
  opacity: 0.6;
}

.upload-text {
  font-size: 30rpx;
  color: $text-main;
  font-weight: 600;
}

.upload-hint {
  font-size: 24rpx;
  color: $text-sub;
  margin-top: 8rpx;
}

.preview-img {
  width: 100%;
  height: 100%;
}

.re-upload-btn {
  position: absolute;
  bottom: 24rpx;
  right: 24rpx;
  background: rgba(0,0,0,0.6);
  color: #fff;
  font-size: 24rpx;
  padding: 8rpx 20rpx;
  border-radius: 99rpx;
}

.full-btn {
  width: 100%;
  margin-bottom: 40rpx;
  
  &.disabled {
    background: #9CA3AF;
  }
}

.result-card {
  padding: 32rpx;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(20rpx); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.result-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $text-main;
}

.confidence-tag {
  background: $primary-light;
  color: $primary-dark;
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 8rpx;
  font-weight: 600;
}

.result-row {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.label {
  font-size: 28rpx;
  color: $text-sub;
  width: 160rpx;
}

.value {
  font-size: 30rpx;
  color: $text-main;
  font-weight: 500;
  
  &.highlight {
    color: $danger;
    font-weight: 700;
    font-size: 32rpx;
  }
}

.divider {
  height: 2rpx;
  background: #F3F4F6;
  margin: 24rpx 0;
}

.advice-section {
  display: flex;
  flex-direction: column;
}

.advice-text {
  margin-top: 12rpx;
  font-size: 28rpx;
  color: $text-main;
  line-height: 1.6;
  background: #F9FAFB;
  padding: 16rpx;
  border-radius: 12rpx;
}

.error-msg {
  text-align: center;
  color: $danger;
  font-size: 26rpx;
  margin-top: 20rpx;
}
</style>
