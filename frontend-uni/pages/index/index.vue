<template>
  <view class="page-container">
    <!-- Top Header -->
    <view class="dashboard-header">
      <view class="header-content">
        <text class="greeting">{{ greetingText }}，{{ userName }}</text>
        <text class="title-lg text-white">茶园总览</text>
      </view>
      <view class="weather-widget">
        <text class="weather-temp">{{ weather.temperature }}°C</text>
        <text class="weather-desc">{{ weather.weather }}</text>
      </view>
    </view>

    <!-- Stats Grid -->
    <view class="stats-grid">
      <view class="stat-card">
        <text class="stat-val">{{ stats.garden_count }}</text>
        <text class="stat-label">茶园总数</text>
      </view>
      <view class="stat-card">
        <text class="stat-val">{{ stats.device_online_count }}</text>
        <text class="stat-label">设备在线</text>
      </view>
      <view class="stat-card" :class="{ warning: stats.alarm_count > 0 }">
        <text class="stat-val">{{ stats.alarm_count }}</text>
        <text class="stat-label">当前告警</text>
      </view>
    </view>

    <!-- Garden List -->
    <view class="section-title">
      <text class="title-md">我的茶园</text>
      <text class="text-sub">全部 ></text>
    </view>

    <view class="garden-list">
      <view v-for="item in gardens" :key="item.id" class="card garden-card" @click="goDetail(item.id)">
        <image class="garden-cover" :src="item.image" mode="aspectFill"></image>
        <view class="garden-info">
          <view class="info-header">
            <text class="garden-name">{{ item.name }}</text>
            <view class="tag" :class="item.status === 'normal' ? 'tag-primary' : 'tag-warn'">
              {{ item.status === 'normal' ? '正常运行' : '需关注' }}
            </view>
          </view>
          
          <view class="info-metrics">
            <view class="metric-item">
              <text class="metric-val">{{ item.area }}亩</text>
              <text class="metric-label">面积</text>
            </view>
            <view class="metric-divider"></view>
            <view class="metric-item">
              <text class="metric-val">{{ item.devices }}台</text>
              <text class="metric-label">设备</text>
            </view>
          </view>
          
          <view v-if="item.lastAlert" class="alert-preview">
            <text class="alert-icon">⚠️</text>
            <text class="alert-text">{{ item.lastAlert }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getDashboardStats } from '@/api/dashboard.js';
import { getGardenList } from '@/api/garden.js';
import { getWeather } from '@/api/weather.js';

export default {
  data() {
    return {
      stats: {
        garden_count: 0,
        device_online_count: 0,
        alarm_count: 0
      },
      gardens: [],
      loading: false,
      loading: false,
      userName: '管理员',
      weather: {
        temperature: '--',
        weather: '获取中...'
      }
    };
  },
  onShow() {
      const userInfo = uni.getStorageSync('userInfo');
      if (userInfo && (userInfo.name || userInfo.username)) {
          this.userName = userInfo.name || userInfo.username;
      }
      this.loadData();
  },
  onPullDownRefresh() {
    this.loadData();
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        // 1. Load core data (Fast)
        const [statsRes, gardensRes] = await Promise.all([
          getDashboardStats(),
          getGardenList({ page: 1, size: 100 })
        ]);

        this.stats = statsRes;
        this.gardens = gardensRes.list.map(item => ({
          ...item,
          devices: item.totalCount || 0,
          image: item.image_path ? (this.$baseUrl + item.image_path) : '/static/default_garden.jpg', 
          lastAlert: item.alarmCount > 0 ? `${item.alarmCount}条告警待处理` : null
        }));

        // 2. Load weather asynchronously (Slow, don't block)
        getWeather('信阳').then(res => {
            if (res) this.weather = res;
        }).catch(e => console.error('Weather load failed', e));

        // 3. Silent Prefetch for gardens (Populate cache for Detail Page)
        this.gardens.forEach(g => {
            const loc = g.address || g.name || '信阳';
            getWeather(loc).catch(() => {}); // Just cache it, ignore result/error
        });
        
      } catch (e) {
        console.error(e);
        uni.showToast({ title: '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
        uni.stopPullDownRefresh();
      }
    },
    goDetail(id) {
      // Navigate to Garden Detail (Plot List)
      uni.navigateTo({ url: `/pages/plot/index?garden_id=${id}` });
    }
  },
  computed: {
    greetingText() {
        const hour = new Date().getHours();
        if (hour < 6) return '夜深了';
        if (hour < 9) return '早上好';
        if (hour < 12) return '上午好';
        if (hour < 14) return '中午好';
        if (hour < 18) return '下午好';
        return '晚上好';
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.greeting {
  font-size: 24rpx;
  color: $text-sub;
  margin-bottom: 8rpx;
  display: block;
}

.weather-widget {
  text-align: right;
}

.weather-temp {
  font-size: 36rpx;
  font-weight: 700;
  color: $primary;
  display: block;
}

.weather-desc {
  font-size: 24rpx;
  color: $text-sub;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
  margin-bottom: 40rpx;
}

.stat-card {
  background: #fff;
  padding: 24rpx;
  border-radius: 20rpx;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.03);
  
  &.warning {
    background: #FEF3C7;
    .stat-val { color: #D97706; }
  }
}

.stat-val {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $text-main;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: $text-sub;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.garden-card {
  padding: 0; // Reset default padding
  overflow: hidden;
}

.garden-cover {
  width: 100%;
  height: 240rpx;
  background-color: #E5E7EB;
}

.garden-info {
  padding: 24rpx;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.garden-name {
  font-size: 32rpx;
  font-weight: 700;
  color: $text-main;
}

.info-metrics {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 24rpx;
}

.metric-item {
  text-align: center;
}

.metric-val {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: $text-main;
}

.metric-label {
  font-size: 22rpx;
  color: $text-sub;
}

.metric-divider {
  width: 2rpx;
  height: 24rpx;
  background: #E5E7EB;
}

.alert-preview {
  background: #FEF2F2;
  padding: 16rpx;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.alert-icon {
  font-size: 24rpx;
}

.alert-text {
  font-size: 24rpx;
  color: #DC2626;
}
</style>
