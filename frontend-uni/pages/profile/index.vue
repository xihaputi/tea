<template>
  <view class="page-container">
    <view class="title-lg header">我的</view>

    <!-- 未登录状态 -->
    <view v-if="!isLoggedIn" class="login-box card">
      <view class="title-md" style="margin-bottom: 32rpx; text-align: center;">账号登录</view>
      <input class="input" v-model="loginForm.username" placeholder="请输入用户名" />
      <input class="input" v-model="loginForm.password" password placeholder="请输入密码" />
      <button class="btn-primary" @click="handleLogin" :loading="loading">登录</button>
    </view>

    <!-- 已登录状态 -->
    <view v-else>
      <view class="card profile-card">
        <view class="avatar-placeholder">{{ user.name ? user.name[0] : 'U' }}</view>
        <view class="info">
          <text class="name">{{ user.name || user.username }}</text>
          <text class="role">{{ user.roles ? user.roles.join(', ') : '普通用户' }}</text>
        </view>
      </view>

      <view class="card menu-list">
        <view class="menu-item" @click="showToast('功能开发中')">
          <text>账号设置</text>
          <text class="arrow">></text>
        </view>
        <view class="menu-item" @click="showToast('功能开发中')">
          <text>关于我们</text>
          <text class="arrow">></text>
        </view>
      </view>

      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script>
import { login, getUserInfo, logout } from '@/api/auth.js';

export default {
  data() {
    return {
      isLoggedIn: false,
      loading: false,
      user: {},
      loginForm: {
        username: '',
        password: ''
      }
    };
  },
  onShow() {
    this.checkLogin();
  },
  methods: {
    checkLogin() {
      const token = uni.getStorageSync('token');
      if (token) {
        this.isLoggedIn = true;
        this.fetchUserInfo();
      } else {
        this.isLoggedIn = false;
        this.user = {};
      }
    },
    async fetchUserInfo() {
      try {
        const res = await getUserInfo();
        this.user = res;
      } catch (e) {
        // Token invalid
        this.isLoggedIn = false;
        uni.removeStorageSync('token');
      }
    },
    async handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) {
        uni.showToast({ title: '请输入账号密码', icon: 'none' });
        return;
      }
      this.loading = true;
      try {
        const res = await login(this.loginForm);
        uni.setStorageSync('token', res.token);
        this.isLoggedIn = true;
        this.user = res.userInfo;
        uni.showToast({ title: '登录成功', icon: 'success' });
      } catch (e) {
        uni.showToast({ title: e.detail || '登录失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    async handleLogout() {
      try {
        await logout();
      } catch (e) {}
      uni.removeStorageSync('token');
      this.isLoggedIn = false;
      this.user = {};
      this.loginForm = { username: '', password: '' };
    },
    showToast(msg) {
      uni.showToast({ title: msg, icon: 'none' });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.header {
  padding: 24rpx 0;
}

.login-box {
  padding: 40rpx;
  margin-top: 40rpx;
}

.input {
  background: #F9FAFB;
  border: 2rpx solid #E5E7EB;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 24rpx;
  font-size: 28rpx;
}

.profile-card {
  display: flex;
  align-items: center;
  padding: 40rpx;
}

.avatar-placeholder {
  width: 100rpx;
  height: 100rpx;
  background: $primary-light;
  color: $primary;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  font-weight: 700;
  margin-right: 24rpx;
}

.info {
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 32rpx;
  font-weight: 700;
  color: $text-main;
}

.role {
  font-size: 24rpx;
  color: $text-sub;
  margin-top: 8rpx;
}

.menu-list {
  padding: 0 24rpx;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  padding: 32rpx 0;
  border-bottom: 2rpx solid #F3F4F6;
  font-size: 28rpx;
  color: $text-main;
  
  &:last-child {
    border-bottom: none;
  }
}

.logout-btn {
  margin-top: 40rpx;
  background: #FEE2E2;
  color: #DC2626;
  font-size: 28rpx;
  border-radius: 16rpx;
  
  &::after {
    border: none;
  }
}
</style>
