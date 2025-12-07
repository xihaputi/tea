<template>
  <view class="page-container">
    <!-- Header -->
    <view class="header">
      <text class="title-lg">事务中心</text>
      <view class="top-segment">
          <view 
            class="segment-item" 
            :class="{ active: activeModule === 'alarm' }"
            @click="switchModule('alarm')"
          >
            告警信息
          </view>
          <view 
            class="segment-item" 
            :class="{ active: activeModule === 'task' }"
            @click="switchModule('task')"
          >
            待办事项
          </view>
      </view>
    </view>
    
    <!-- Sub Tabs for Alarm -->
    <view class="filter-tabs" v-if="activeModule === 'alarm'">
        <view 
          v-for="(t, i) in alarmTabs" 
          :key="i"
          class="tab-item"
          :class="{ active: currentAlarmTab === i }"
          @click="currentAlarmTab = i"
        >
          {{ t }}
        </view>
    </view>

    <!-- Content Area -->
    <view class="content-area">
        
        <!-- ALARM LIST -->
        <template v-if="activeModule === 'alarm'">
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
            <!-- Alarm Empty States -->
            <view class="loading-more" v-if="loading">
                <text>加载中...</text>
            </view>
            <view class="empty" v-if="!loading && alarms.length === 0">
                <image src="/static/empty.png" mode="aspectFit" class="empty-icon" />
                <text>暂无告警信息</text>
            </view>
        </template>

        <!-- TASK LIST -->
        <template v-if="activeModule === 'task'">
             <view v-for="item in tasks" :key="item.id" class="card task-card" @click="handleTask(item)">
                <view class="task-top">
                    <text class="task-title">{{ item.name }}</text>
                    <view class="task-priority" :class="'p-' + (item.priority || 'medium')">
                        {{ priorityText(item.priority) }}
                    </view>
                </view>
                <view class="task-desc">
                    {{ item.description || '暂无描述' }}
                </view>
                <view class="task-meta">
                    <view class="meta-item">
                        <text class="icon">📅</text>
                        <text>{{ formatDate(item.deadline) || '无截止日期' }}</text>
                    </view>
                    <view class="meta-item">
                        <text class="icon">👤</text>
                        <text>{{ item.assignee || '未分配' }}</text>
                    </view>
                </view>
                <view class="task-footer">
                    <view class="status-badge" :class="item.status">
                        {{ item.status === 'completed' ? '已完成' : '进行中' }}
                    </view>
                    <view class="btn-check" @click.stop="completeTask(item)">
                        {{ item.status === 'completed' ? '已归档' : '标记完成' }}
                    </view>
                </view>
             </view>
             
             <!-- Task Empty States -->
            <view class="loading-more" v-if="loading">
                <text>加载中...</text>
            </view>
            <view class="empty" v-if="!loading && tasks.length === 0">
                <image src="/static/empty.png" mode="aspectFit" class="empty-icon" />
                <text>暂无待办任务</text>
            </view>
        </template>

    </view>
  </view>
</template>

<script>
import { getAlarmList, acknowledgeAlarm } from '@/api/alarm.js';
import { getTaskList, updateTask } from '@/api/task.js';

export default {
  data() {
    return {
      activeModule: 'alarm', // 'alarm' or 'task'
      
      // Alarm Data
      alarmTabs: ['未读', '已处理', '全部'],
      currentAlarmTab: 0,
      alarms: [],
      
      // Task Data
      tasks: [],
      
      // Pagination
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
    activeModule() {
        this.resetPagination();
        this.loadData();
    },
    currentAlarmTab() {
        if (this.activeModule === 'alarm') {
            this.resetPagination();
            this.loadData();
        }
    }
  },
  methods: {
    switchModule(mod) {
        this.activeModule = mod;
    },
    resetPagination() {
        this.page = 1;
        this.hasMore = true;
        this.alarms = [];
        this.tasks = [];
    },
    async loadData() {
      if (this.loading) return;
      this.loading = true;
      
      try {
        if (this.activeModule === 'alarm') {
            await this.loadAlarms();
        } else {
            await this.loadTasks();
        }
      } catch (e) {
        console.error(e);
        uni.showToast({ title: '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
        if (this.isRefreshing) {
            this.isRefreshing = false;
            uni.stopPullDownRefresh();
        }
      }
    },
    
    async loadAlarms() {
        // Map tab index to API status
        // 0: Unread (active), 1: Cleared, 2: All
        let status = '';
        if (this.currentAlarmTab === 0) status = 'active';
        else if (this.currentAlarmTab === 1) status = 'cleared';
        
        const res = await getAlarmList({
          page: this.page,
          size: this.pageSize,
          status: status
        });
        
        const list = res.list || [];
        if (this.page === 1) this.alarms = list;
        else this.alarms = [...this.alarms, ...list];
        
        this.total = res.total || 0;
        this.hasMore = this.alarms.length < this.total;
    },
    
    async loadTasks() {
        const res = await getTaskList({
            page: this.page,
            size: this.pageSize,
            status: 'pending' // Default load pending tasks? Or all? Let's load all for now or handled by backend default
        });
        
        // Backend task API might return structure differently. Assuming format { list, total }
        // If not, adjust accordingly. Web api usually returns { list: [], total: 0 }
        
        const list = res.list || [];
        if (this.page === 1) this.tasks = list;
        else this.tasks = [...this.tasks, ...list];
        
        this.total = res.total || 0;
        this.hasMore = this.tasks.length < this.total;
    },

    // Alarm Helpers
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
      if (item.status !== 'active') return;
      uni.showActionSheet({
        itemList: ['标记为已处理'],
        success: async (res) => {
          if (res.tapIndex === 0) {
            try {
                await acknowledgeAlarm(item.id);
                uni.showToast({ title: '已标志处理', icon: 'success' });
                // 刷新列表
                this.resetPagination();
                this.loadData();
            } catch (e) {
                uni.showToast({ title: '操作失败', icon: 'none' });
            }
          }
        }
      });
    },

    // Task Helpers
    priorityText(p) {
        const map = { high: '高', medium: '中', low: '低' };
        return map[p] || '普通';
    },
    formatDate(d) {
        if (!d) return '';
        return new Date(d).toLocaleDateString();
    },
    async completeTask(item) {
        if (item.status === 'completed') return;
        uni.showModal({
            title: '确认',
            content: '确定标记该任务为已完成吗？',
            success: async (res) => {
                if (res.confirm) {
                    try {
                        await updateTask(item.id, { status: 'completed' });
                        uni.showToast({ title: '任务已完成' });
                        this.resetPagination();
                        this.loadData();
                    } catch(e) {
                        uni.showToast({ title: '操作失败', icon: 'none' });
                    }
                }
            }
        })
    },
    handleTask(item) {
        // Go to task detail
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page-container {
    padding: 24rpx;
    background-color: #F9FAFB;
    min-height: 100vh;
}

.header {
  margin-bottom: 32rpx;
}
.title-lg {
    font-size: 40rpx;
    font-weight: 700;
    color: #111;
    display: block;
    margin-bottom: 24rpx;
}

.top-segment {
    display: flex;
    background: #E5E7EB;
    border-radius: 16rpx;
    padding: 6rpx;
}
.segment-item {
    flex: 1;
    text-align: center;
    padding: 16rpx 0;
    font-size: 28rpx;
    color: #6B7280;
    border-radius: 12rpx;
    transition: all 0.3s;
    font-weight: 500;
    
    &.active {
        background: #fff;
        color: #10B981;
        box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.05);
        font-weight: 600;
    }
}

.filter-tabs {
  display: flex;
  margin-bottom: 24rpx;
  justify-content: flex-start;
  gap: 20rpx;
}

.tab-item {
  padding: 8rpx 24rpx;
  font-size: 26rpx;
  color: #6B7280;
  border-radius: 30rpx;
  background: #fff;
  border: 1rpx solid #E5E7EB;
  
  &.active {
    background: #10B981;
    color: #fff;
    border-color: #10B981;
  }
}

/* Alarm Card Styles */
.alarm-card {
  margin-bottom: 20rpx;
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.03);
}

.card-top {
  display: flex;
  justify-content: space-between;
  padding: 24rpx;
  border-bottom: 1rpx solid #F3F4F6;
}

.garden-name {
  font-weight: 600;
  font-size: 28rpx;
  color: #374151;
}

.device-name {
  font-size: 24rpx;
  color: #9CA3AF;
}

.time {
  font-size: 24rpx;
  color: #9CA3AF;
}

.card-content {
  display: flex;
  align-items: center;
  padding: 24rpx;
}

.severity-indicator {
  width: 8rpx;
  height: 60rpx;
  border-radius: 4rpx;
  margin-right: 24rpx;
  flex-shrink: 0;
  
  &.bg-critical { background: #EF4444; }
  &.bg-warning { background: #F59E0B; }
  &.bg-info { background: #3B82F6; }
}

.alarm-text {
  font-size: 28rpx;
  color: #374151;
  line-height: 1.5;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 24rpx;
  background: #F9FAFB;
}

.tag {
    padding: 4rpx 12rpx;
    border-radius: 8rpx;
    font-size: 22rpx;
    
    &.tag-danger { background: #FEE2E2; color: #EF4444; }
    &.tag-primary { background: #D1FAE5; color: #10B981; }
}

.action-btn {
  font-size: 26rpx;
  color: #10B981;
  font-weight: 600;
}

/* Task Card Styles */
.task-card {
    background: #fff;
    border-radius: 20rpx;
    padding: 24rpx;
    margin-bottom: 20rpx;
    border-left: 8rpx solid #10B981;
    box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.03);
}

.task-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16rpx;
}

.task-title {
    font-size: 32rpx;
    font-weight: 600;
    color: #1F2937;
    flex: 1;
}

.task-priority {
    font-size: 22rpx;
    padding: 4rpx 12rpx;
    border-radius: 8rpx;
    margin-left: 16rpx;
    flex-shrink: 0;
    
    &.p-high { background: #FEE2E2; color: #EF4444; }
    &.p-medium { background: #FEF3C7; color: #D97706; }
    &.p-low { background: #E0F2FE; color: #0284C7; }
}

.task-desc {
    font-size: 28rpx;
    color: #6B7280;
    margin-bottom: 20rpx;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.task-meta {
    display: flex;
    gap: 24rpx;
    margin-bottom: 24rpx;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
    font-size: 24rpx;
    color: #9CA3AF;
}

.task-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16rpx;
    border-top: 1rpx solid #F3F4F6;
}

.status-badge {
    font-size: 24rpx;
    color: #6B7280;
    
    &.completed { color: #10B981; }
}

.btn-check {
    font-size: 26rpx;
    color: #10B981;
    font-weight: 600;
    padding: 8rpx 16rpx;
    background: #ECFDF5;
    border-radius: 30rpx;
}

/* Common */
.empty {
    padding: 60rpx 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .empty-icon { width: 200rpx; height: 200rpx; margin-bottom: 20rpx; opacity: 0.5; }
    text { color: #9CA3AF; font-size: 28rpx; }
}

.loading-more {
    text-align: center;
    padding: 20rpx;
    color: #9CA3AF;
    font-size: 24rpx;
}
</style>
