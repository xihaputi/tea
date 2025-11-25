<template>
  <view class="page">
    <!-- 顶部筛选 -->
    <view class="top-bar">
      <picker mode="selector" :range="groups" @change="changeGroup">
        <view class="top-item">
          {{ groups[currentGroup] }}
          <text class="arrow">▼</text>
        </view>
      </picker>
      <view class="top-item tag-active">全部</view>
      <picker mode="selector" :range="statusFilters" @change="changeStatus">
        <view class="top-item">
          筛选
          <text class="arrow">▼</text>
        </view>
      </picker>
    </view>

    <!-- 地块卡片 -->
    <view v-for="plot in plots" :key="plot.id" class="card">
      <view class="card-header">
        <text class="card-title">{{ plot.name }}</text>
        <text class="status" :class="statusClass(plot.status)">状态：{{ statusText(plot.status) }}</text>
      </view>

      <view class="row">面积：{{ plot.area }} 亩 · 海拔：{{ plot.altitude }}m</view>
      <view class="row">墒情湿度：{{ plot.moisture }}% · pH：{{ plot.ph }}</view>
      <view class="row">已安装设备：{{ plot.devices }} 台（{{ plot.deviceDesc }}）</view>

      <view class="card-actions">
        <view class="action" @click="goDetail(plot.id)">⚪ 详情</view>
        <view class="action" @click="goAdvice(plot.id)">🤖 AI 方案</view>
        <view class="action" @click="editPlot(plot.id)">✎ 编辑</view>
        <view class="action" @click="goHistory(plot.id)">🕑 历史</view>
      </view>
    </view>

    
  </view>
</template>

<script>
export default {
  data() {
    return {
      groups: ['当前茶园 / 合作社'],
      currentGroup: 0,
      statusFilters: ['全部', '正常', '预警', '告警'],
      currentStatus: 0,
      plots: [
        {
          id: 1,
          name: '1号地块·龙井43',
          status: 'dry',
          area: 3.5,
          altitude: 320,
          moisture: 23,
          ph: 5.4,
          devices: 3,
          deviceDesc: '传感器2 + 摄像头1',
        },
        {
          id: 2,
          name: '2号地块·福鼎',
          status: 'normal',
          area: 4.2,
          altitude: 280,
          moisture: 55,
          ph: 5.7,
          devices: 4,
          deviceDesc: '传感器3 + 摄像头1',
        },
      ],
    };
  },
  methods: {
    changeGroup(e) {
      this.currentGroup = e.detail.value;
    },
    changeStatus(e) {
      this.currentStatus = e.detail.value;
    },
    statusText(status) {
      if (status == 'dry') return '轻度缺水';
      if (status == 'alert') return '告警';
      return '正常';
    },
    statusClass(status) {
      if (status == 'dry') return 'status-warn';
      if (status == 'alert') return 'status-alert';
      return 'status-normal';
    },
    goDetail(id) {
      uni.navigateTo({ url: `/pages/plot/detail?plot_id=${id}` });
    },
    goHistory(id) {
      uni.navigateTo({ url: `/pages/stats/stats?plot_id=${id || ''}` });
    },
    goAdvice(id) {
      uni.navigateTo({ url: `/pages/advice/index?plot_id=${id || ''}` });
    },
    editPlot(id) {
      uni.showToast({ title: '编辑（占位）', icon: 'none' });
    },
  },
};
</script>

<style scoped lang="scss">
.page {
  padding: 20rpx 24rpx 120rpx;
  background: #f6f8fb;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  font-size: 32rpx;
  font-weight: 700;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 20rpx;
  color: #167c4a;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.top-item,
.filter-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 0;
}

.tag-active,
.filter-item.active {
  border-bottom: 2rpx solid #167c4a;
}

.arrow {
  font-size: 24rpx;
}

.card {
  background: #fafff8;
  border: 2rpx solid #c7ebd6;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 10rpx rgba(22, 124, 74, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: 700;
}

.status {
  font-size: 26rpx;
}

.status-normal { color: #16a34a; }
.status-warn { color: #f59e0b; }
.status-alert { color: #ef4444; }

.row {
  margin: 6rpx 0;
  color: #2f3c3b;
  font-size: 26rpx;
}

.card-actions {
  margin-top: 16rpx;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12rpx;
  color: #167c4a;
  font-weight: 600;
  font-size: 26rpx;
}

.action {
  text-align: center;
  padding: 8rpx 0;
  border-radius: 12rpx;
  background: #e8f5ee;
}

.quick-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
  margin-top: 12rpx;
}

.quick-card {
  background: #f0fff6;
  border: 2rpx solid #c7ebd6;
  border-radius: 16rpx;
  padding: 20rpx;
  text-align: center;
  color: #167c4a;
}

.quick-title {
  font-size: 30rpx;
  font-weight: 700;
}

.quick-sub {
  display: block;
  margin-top: 6rpx;
  font-size: 24rpx;
}
</style>
