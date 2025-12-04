<template>
  <view class="page-container">
    <!-- Header -->
    <view class="header">
      <text class="title-lg">告警中心</text>
      <view class="filter-tabs">
        <view 
          v-for="(tab, index) in tabs" 
          :key="index"
          class="tab-item"
          :class="{ active: currentTab === index }"
          @click="currentTab = index"
        >
          {{ tab }}
        </view>
      </view>
    </view>

    <!-- Alarm List -->
    <view class="alarm-list">
      <view v-for="item in alarms" :key="item.id" class="card alarm-card">
        <view class="card-top">
          <view class="garden-info">
            <text class="garden-name">{{ item.gardenName || '未知茶园' }}</text>
            <text class="device-name"> · {{ item.deviceName || '未知设备' }}</text>
          </view>
          <text class="time">{{ item.created_at }}</text>
        </view>
        
        <view class="card-content">
          <view class="severity-indicator" :class="severityClass(item.severity)"></view>
          <text class="alarm-text">{{ item.content }}</text>
        </view>
        
        <view class="card-actions">
          <view class="tag" :class="statusTagClass(item.status)">
            {{ statusText(item.status) }}
          </view>
          <view class="action-btn" @click="handleAlarm(item)">
            处理 >
          </view>
        </view>
      </view>
      
      <!-- Loading / Empty State -->
      <view class="loading-more" v-if="loading">
        <text>加载中...</text>
      </view>
      <view class="no-more" v-if="!hasMore && alarms.length > 0">
        <text>没有更多了</text>
      </view>
      <view class="empty" v-if="!loading && alarms.length === 0">
        <text>暂无告警信息</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getAlarmList } from '@/api/alarm.js';

export default {
  data() {
    return {
      tabs: ['全部', '未读', '已处理'],
      currentTab: 0,
      alarms: [],
      page: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      hasMore: true,
      isRefreshing: false
    }
  },
  onLoad() {
    this.loadData();
  },
  onPullDownRefresh() {
    this.isRefreshing = true;
    this.page = 1;
    this.hasMore = true;
    this.loadData();
  },
  onReachBottom() {
    if (this.hasMore && !this.loading) {
      this.page++;
      this.loadData();
    }
  },
  watch: {
    currentTab() {
      this.page = 1;
      this.hasMore = true;
      this.alarms = [];
      this.loadData();
    }
  },
  methods: {
    async loadData() {
      if (this.loading) return;
      this.loading = true;
      
      try {
        const statusMap = { 0: '', 1: 'active', 2: 'cleared' };
        const status = statusMap[this.currentTab];
        
        const res = await getAlarmList({
          page: this.page,
          size: this.pageSize,
          status: status
        });
        
        if (this.isRefreshing || this.page === 1) {
          this.alarms = res.list;
          this.isRefreshing = false;
          uni.stopPullDownRefresh();
        } else {
          this.alarms = [...this.alarms, ...res.list];
        }
        
        this.total = res.total;
        this.hasMore = this.alarms.length < this.total;
        
      } catch (e) {
        console.error(e);
        uni.showToast({ title: '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    severityClass(severity) {
      if (severity === 'critical') return 'bg-critical';
      if (severity === 'warning') return 'bg-warning';
      return 'bg-info';
    },
    statusTagClass(status) {
      if (status === 'active') return 'tag-danger';
      return 'tag-primary';
    },
    statusText(status) {
      return status === 'active' ? '待处理' : '已恢复';
    },
    handleAlarm(item) {
      // Go to detail or show action sheet
      uni.showActionSheet({
        itemList: ['标记为已处理', '查看详情'],
        success: (res) => {
          if (res.tapIndex === 0) {
            // Call API to update status (mock for now or implement)
            uni.showToast({ title: '已标记处理', icon: 'success' });
          } else {
             uni.navigateTo({ url: `/pages/alarm/detail?id=${item.id}` });
          }
        }
      });
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.header {
  margin-bottom: 32rpx;
}

.filter-tabs {
  display: flex;
  margin-top: 24rpx;
  background: #fff;
  padding: 8rpx;
  border-radius: 16rpx;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 12rpx 0;
  font-size: 28rpx;
  color: $text-sub;
  border-radius: 12rpx;
  transition: all 0.3s;
  
  &.active {
    background: $primary;
    color: #fff;
    font-weight: 600;
    box-shadow: 0 4rpx 12rpx rgba(16, 185, 129, 0.2);
  }
}

.alarm-card {
  position: relative;
  overflow: hidden;
}

.card-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.garden-name {
  font-weight: 600;
  font-size: 28rpx;
  color: $text-main;
}

.device-name {
  font-size: 24rpx;
  color: $text-sub;
}

.time {
  font-size: 24rpx;
  color: $text-sub;
}

.card-content {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
  padding: 24rpx;
  background: #F9FAFB;
  border-radius: 12rpx;
}

.severity-indicator {
  width: 8rpx;
  height: 60rpx;
  border-radius: 4rpx;
  margin-right: 20rpx;
  
  &.bg-critical { background: #EF4444; }
  &.bg-warning { background: #F59E0B; }
  &.bg-info { background: #3B82F6; }
}

.alarm-text {
  font-size: 28rpx;
  color: $text-main;
  line-height: 1.4;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 2rpx solid #F3F4F6;
}

.action-btn {
  font-size: 26rpx;
  color: $primary;
  font-weight: 600;
}
</style>
