<template>
  <view class="page">
    <view class="title" style="padding: 24rpx 24rpx 8rpx">茶园总览</view>
    <view class="subtitle" style="padding: 0 24rpx 16rpx">核心地块与当前状态</view>
    <view v-if="error" class="card" style="color: #ef4444">{{ error }}</view>
    <view v-if="loading" class="card">加载中...</view>
    <view v-for="plot in plots" :key="plot.id" class="card">
      <view class="title">{{ plot.name }}</view>
      <view class="subtitle">{{ plot.location || '未填写位置' }}</view>
      <view style="margin: 12rpx 0">
        <text class="pill" :class="statusClass(plot.status)">{{ statusLabel(plot.status) }}</text>
      </view>
      <view class="btn-primary" @click="goDetail(plot.id)">查看详情</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../common/http.js';

export default {
  data() {
    return {
      plots: [],
      loading: false,
      error: '',
    };
  },
  onLoad() {
    this.fetchPlots();
  },
  methods: {
    async fetchPlots() {
      this.loading = true;
      this.error = '';
      try {
        this.plots = await api.get('/plots');
      } catch (e) {
        this.error = '加载地块失败，请检查后端服务';
      } finally {
        this.loading = false;
      }
    },
    statusClass(status) {
      if (status === 'optimal') return 'pill-optimal';
      if (status?.includes('moisture-low')) return 'pill-water';
      if (status?.includes('wet')) return 'pill-drain';
      return 'pill-optimal';
    },
    statusLabel(status) {
      if (status === 'optimal') return '适宜';
      if (status?.includes('moisture-low')) return '偏干';
      if (status?.includes('wet')) return '偏湿';
      return status || '未知';
    },
    goDetail(plotId) {
      uni.navigateTo({ url: `/pages/plot/detail?plot_id=${plotId}` });
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
</style>
