<template>
  <view class="page-container">
    <!-- Header Background -->
    <view class="profile-header">
      <view class="title-lg text-white">个人中心</view>
    </view>
    
    <view class="profile-content">
      <!-- User Card -->
      <view class="card user-card">
        <view class="avatar-box">
          <text class="avatar-text">{{ user.name ? user.name[0] : (user.username ? user.username[0] : 'U') }}</text>
        </view>
        <view class="user-info">
          <text class="user-name">{{ user.name || user.username }}</text>
          <view class="user-role-tag">
            {{ user.roles ? user.roles.join(', ') : '普通用户' }}
          </view>
        </view>
        <view class="edit-btn" @click="showToast('编辑功能开发中')">✎</view>
      </view>

      <!-- Menu List -->
      <view class="card menu-card">
        <view class="menu-item" @click="showToast('账号安全功能开发中')">
          <view class="menu-left">
            <text class="menu-icon">🛡️</text>
            <text class="menu-text">账号与安全</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-divider"></view>
        <view class="menu-item" @click="showToast('系统设置功能开发中')">
          <view class="menu-left">
            <text class="menu-icon">⚙️</text>
            <text class="menu-text">系统设置</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-divider"></view>
        <view class="menu-item" @click="showToast('关于我们功能开发中')">
          <view class="menu-left">
            <text class="menu-icon">ℹ️</text>
            <text class="menu-text">关于我们</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>

      <button class="btn-logout" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script>
import { getUserInfo, logout } from '@/api/auth.js';

export default {
  data() {
    return {
      user: {}
    };
  },
  onShow() {
    this.loadUserInfo();
  },
  methods: {
    async loadUserInfo() {
      // We assume token exists because app forces login
      try {
        const res = await getUserInfo();
        this.user = res;
      } catch (e) {
        // If getting user info fails (e.g. 401), HTTP interceptor will handle redirect
        // But we can also handle it partly here
      }
    },
    async handleLogout() {
      try {
        await logout();
      } catch (e) {}
      uni.removeStorageSync('token');
      uni.removeStorageSync('userInfo');
      
      // Force redirect to login
      uni.reLaunch({ url: '/pages/login/index' });
    },
    showToast(msg) {
      uni.showToast({ title: msg, icon: 'none' });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page-container {
  padding: 0;
  background-color: $bg-page;
  min-height: 100vh;
}

/* Header with Green Background */
.profile-header {
  height: 300rpx;
  background: linear-gradient(180deg, $primary-dark 0%, $primary 100%);
  padding: 88rpx 32rpx 0;
}

.profile-content {
  padding: 0 32rpx;
  margin-top: -100rpx; /* Pull up to overlap header */
  padding-bottom: 40rpx;
}

/* User Card */
.user-card {
  display: flex;
  align-items: center;
  padding: 40rpx;
  margin-bottom: 32rpx;
}

.avatar-box {
  width: 120rpx;
  height: 120rpx;
  background: $primary-light;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 32rpx;
  border: 4rpx solid #fff;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
  
  &.placeholder {
    background: #E5E7EB;
    color: #9CA3AF;
  }
}

.avatar-text {
  font-size: 48rpx;
  font-weight: 700;
  color: $primary-dark;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 36rpx;
  font-weight: 700;
  color: $text-main;
  display: block;
  margin-bottom: 8rpx;
}

.user-role-tag {
  display: inline-block;
  font-size: 22rpx;
  background: $primary-light;
  color: $primary-dark;
  padding: 4rpx 16rpx;
  border-radius: 999rpx;
  font-weight: 600;
}

.user-desc {
  font-size: 26rpx;
  color: $text-sub;
}

.edit-btn {
  color: $text-sub;
  font-size: 36rpx;
  padding: 10rpx;
}

.login-prompt {
  display: flex;
  align-items: center;
  width: 100%;
}

.login-btn {
  background: $primary;
  color: #fff;
  font-size: 26rpx;
  padding: 12rpx 32rpx;
  border-radius: 999rpx;
  font-weight: 600;
}

/* Menu List */
.menu-card {
  padding: 0 32rpx;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 36rpx 0;
  
  &:active { opacity: 0.7; }
}

.menu-left {
  display: flex;
  align-items: center;
}

.menu-icon {
  font-size: 36rpx;
  margin-right: 24rpx;
  width: 48rpx;
  text-align: center;
}

.menu-text {
  font-size: 30rpx;
  color: $text-main;
  font-weight: 500;
}

.menu-arrow {
  color: #D1D5DB;
  font-size: 40rpx;
  line-height: 1;
}

.menu-divider {
  height: 2rpx;
  background: #F3F4F6;
}

/* Logout Button */
.btn-logout {
  margin-top: 48rpx;
  background: #fff;
  color: #EF4444;
  font-size: 30rpx;
  font-weight: 600;
  border-radius: 20rpx;
  padding: 24rpx;
  
  &::after { border: none; }
  &:active { background: #FEF2F2; }
}

/* Login Modal */
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.login-modal {
  width: 80%;
  padding: 48rpx;
}

.modal-title {
  font-size: 40rpx;
  font-weight: 700;
  text-align: center;
  margin-bottom: 48rpx;
  color: $text-main;
}

.input-field {
  background: #F9FAFB;
  border: 2rpx solid #E5E7EB;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  font-size: 28rpx;
  color: $text-main;
  
  &:focus {
    border-color: $primary;
  }
}

.full-width {
  width: 100%;
  margin-top: 24rpx;
}

.text-center {
  text-align: center;
}
</style>
