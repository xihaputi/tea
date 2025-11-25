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
      <picker mode="selector" :range="filters" @change="changeFilter">
        <view class="top-item">
          筛选
          <text class="arrow">▼</text>
        </view>
      </picker>
    </view>

    <!-- 茶园卡片 -->
    <view v-for="item in gardens" :key="item.id" class="card">
      <view class="card-header">
        <text class="card-title">{{ item.name }}</text>
        <view class="header-icons">
          <text class="icon-btn">⟳</text>
          <!-- <text class="icon-btn">✎</text> -->
          <text class="icon-btn">🔖</text>
        </view>
      </view>

      <view class="row">
        <text>编号：{{ item.code }} · 管理员：{{ item.manager }}</text>
      </view>

      <view class="row">
        <text>面积：{{ item.area }} 亩</text>
        <text>地块数量：{{ item.plots }} 块</text>
      </view>

      <view class="row">
        <text>装备设备：{{ item.devices }} 台</text>
        <text>在线：{{ item.online }} 台 · 离线：{{ item.offline }} 台</text>
      </view>

      <view class="row">
        <view class="status">
          <text class="dot" :class="statusDot(item.status)"></text>
          <text>状态：{{ statusText(item.status) }}</text>
        </view>
        <text class="update">最近预警：{{ item.lastAlert }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      groups: ['当前集团 / 合作社'],
      currentGroup: 0,
      filters: ['全部', '正常', '预警', '告警'],
      currentFilter: 0,
      gardens: [
        {
          id: 1,
          name: '茶园 A',
          code: 'TY-001',
          manager: '张三',
          area: 45.2,
          plots: 10,
          devices: 18,
          online: 16,
          offline: 2,
          status: 'normal',
          lastAlert: '2小时前·浇水 (1块地)',
        },
        {
          id: 2,
          name: '茶园 B',
          code: 'TY-002',
          manager: '李四',
          area: 50.0,
          plots: 10,
          devices: 15,
          online: 12,
          offline: 3,
          status: 'normal',
          lastAlert: '3小时前·施肥 (1块地)',
        },
        {
          id: 3,
          name: '茶园 C',
          code: 'TY-003',
          manager: '王五',
          area: 38.5,
          plots: 8,
          devices: 12,
          online: 10,
          offline: 2,
          status: 'warn',
          lastAlert: '1小时前·检查虫害 (1块地)',
        },
      ],
    };
  },
  methods: {
    changeGroup(e) {
      this.currentGroup = e.detail.value;
    },
    changeFilter(e) {
      this.currentFilter = e.detail.value;
    },
    statusText(status) {
      if (status === 'warn') return '预警';
      if (status === 'alert') return '告警';
      return '正常';
    },
    statusDot(status) {
      if (status === 'warn') return 'dot-warn';
      if (status === 'alert') return 'dot-alert';
      return 'dot-normal';
    },
  },
};
</script>

<style lang="scss">
.page {
  padding: 24rpx;
  background: #f6f8fb;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  color: #167c4a;
  font-weight: 600;
}

.top-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 0;
}

.tag-active {
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
  margin-bottom: 16rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
}

.header-icons {
  display: flex;
  gap: 20rpx;
  color: #167c4a;
}

.icon-btn {
  font-size: 30rpx;
}

.row {
  display: flex;
  justify-content: space-between;
  margin: 8rpx 0;
  color: #2f3c3b;
  font-size: 26rpx;
}

.status {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
}

.dot-normal {
  background: #16a34a;
}

.dot-warn {
  background: #f59e0b;
}

.dot-alert {
  background: #ef4444;
}

.update {
  color: #4b5563;
  font-size: 24rpx;
}
</style>
