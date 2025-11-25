<template>
  <view class="page">
    <view class="title" style="padding: 24rpx 24rpx 8rpx">地块详情</view>
    <view class="subtitle" style="padding: 0 24rpx 16rpx">编号 {{ plotId }}</view>

    <view v-if="error" class="card" style="color: #ef4444">{{ error }}</view>
    <view v-if="loading" class="card">加载中...</view>

    <view v-if="sensor" class="card">
      <view class="title">环境数据</view>
      <view class="subtitle">最近记录：{{ formatTime(sensor.timestamp) }}</view>
      <view style="margin-top: 12rpx">
        <view>土壤湿度：{{ sensor.soil_moisture }}%</view>
        <view>气温：{{ sensor.temperature || '--' }} ℃</view>
        <view>湿度：{{ sensor.humidity || '--' }} %</view>
      </view>
    </view>

    <view v-if="advice" class="card">
      <view class="title">今日建议</view>
      <view class="subtitle">基于最新土壤湿度</view>
      <view style="margin: 12rpx 0">
        <text class="pill" :class="pillClass(advice.level)">{{ adviceText(advice.level) }}</text>
      </view>
      <view>{{ advice.advice }}</view>
      <view class="subtitle" style="margin-top: 12rpx">{{ formatTime(advice.timestamp) }}</view>
    </view>

    <view class="card">
      <view class="btn-primary" @click="refresh">刷新数据</view>
    </view>
  </view>
</template>

<script>
import { api } from '../../common/http.js';

export default {
  data() {
    return {
      plotId: null,
      sensor: null,
      advice: null,
      loading: false,
      error: '',
    };
  },
  onLoad(options) {
    this.plotId = Number(options.plot_id);
    this.refresh();
  },
  methods: {
    async refresh() {
      if (!this.plotId) {
        this.error = '未传递地块 ID';
        return;
      }
      this.loading = true;
      this.error = '';
      try {
        const [sensor, advice] = await Promise.all([
          api.get('/sensor/latest', { plot_id: this.plotId }),
          api.get('/advice/today', { plot_id: this.plotId }),
        ]);
        this.sensor = sensor;
        this.advice = advice;
      } catch (e) {
        this.error = '加载失败，请检查后端服务';
      } finally {
        this.loading = false;
      }
    },
    formatTime(ts) {
      if (!ts) return '--';
      return ts.replace('T', ' ').replace('Z', '');
    },
    pillClass(level) {
      if (level === 'optimal') return 'pill-optimal';
      if (level === 'water') return 'pill-water';
      if (level === 'drain') return 'pill-drain';
      return 'pill-optimal';
    },
    adviceText(level) {
      if (level === 'optimal') return '适宜';
      if (level === 'water') return '建议浇水';
      if (level === 'drain') return '注意排水';
      return level || '未知';
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
</style>
