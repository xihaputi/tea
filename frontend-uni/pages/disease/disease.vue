<template>
  <view class="page">
    <view class="title" style="padding: 24rpx 24rpx 8rpx">病虫害诊断</view>
    <view class="subtitle" style="padding: 0 24rpx 16rpx">上传图片，获取快速诊断</view>

    <view v-if="error" class="card" style="color: #ef4444">{{ error }}</view>

    <view class="card">
      <view class="btn-primary" @click="chooseImage">拍照 / 选图</view>
      <view v-if="filePath" style="margin-top: 12rpx">
        <image :src="filePath" mode="widthFix" style="width: 100%" />
      </view>
      <view v-if="uploading" style="margin-top: 12rpx">上传中...</view>
    </view>

    <view v-if="result" class="card">
      <view class="title">诊断结果</view>
      <view style="margin-top: 8rpx">类型：{{ result.disease_type }}</view>
      <view>可信度：{{ (result.confidence * 100).toFixed(1) }}%</view>
      <view style="margin-top: 8rpx">{{ result.advice }}</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../common/http.js';

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
          this.upload();
        },
        fail: () => {
          this.error = '未选择图片';
        },
      });
    },
    async upload() {
      if (!this.filePath) return;
      this.uploading = true;
      this.error = '';
      try {
        this.result = await api.upload('/disease/detect', this.filePath, 'file');
      } catch (e) {
        this.error = '上传或诊断失败，请检查后端';
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
</style>
