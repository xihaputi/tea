<template>
  <view class="login-container">
    <!-- Background Decor -->
    <view class="bg-circle circle-1"></view>
    <view class="bg-circle circle-2"></view>

    <view class="content-wrapper">
      <view class="logo-area">
        <image src="/static/logo.png" mode="aspectFit" class="logo animate-fade-in-down"></image>
        <view class="text-area animate-fade-in-up">
          <text class="app-name">茶智云</text>
          <text class="app-slogan">智慧茶园数字大脑</text>
        </view>
      </view>

      <view class="form-card animate-slide-up">
        <view class="form-header">
          <text class="welcome-text">欢迎登录</text>
        </view>
        
        <view class="input-group">
          <view class="input-icon-wrapper">
            <text class="icon-user">👤</text>
          </view>
          <input class="input" v-model="form.username" placeholder="请输入账号" placeholder-class="input-placeholder" />
        </view>
        
        <view class="input-group">
          <view class="input-icon-wrapper">
            <text class="icon-lock">🔒</text>
          </view>
          <input class="input" v-model="form.password" password placeholder="请输入密码" placeholder-class="input-placeholder" />
        </view>

        <button class="btn-primary" hover-class="btn-hover" @click="handleLogin" :loading="loading">
          立即进入
        </button>
        
        <view class="footer-actions">
           <text class="action-link">忘记密码?</text>
        </view>
      </view>
    </view>
    
    <view class="footer">
      <text class="copyright">Tea Zhi Yun © 2025</text>
    </view>
  </view>
</template>

<script>
import { login } from '@/api/auth.js';

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        uni.showToast({ title: '请输入账号和密码', icon: 'none' });
        return;
      }

      this.loading = true;
      try {
        const res = await login(this.form);
        uni.setStorageSync('token', res.token);
        uni.setStorageSync('userInfo', res.userInfo);
        uni.setStorageSync('roles', res.userInfo.roles || []);
        
        uni.showToast({ title: '登录成功', icon: 'success' });
        
        setTimeout(() => {
          uni.reLaunch({ url: '/pages/index/index' });
        }, 1500);
        
      } catch (e) {
        uni.showToast({ title: e.detail || '登录失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.login-container {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(135deg, #10B981 0%, #047857 100%);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

// Background Decoration
.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  filter: blur(40rpx);
  z-index: 0;
}
.circle-1 {
  width: 400rpx;
  height: 400rpx;
  top: -100rpx;
  right: -100rpx;
}
.circle-2 {
  width: 600rpx;
  height: 600rpx;
  bottom: -200rpx;
  left: -200rpx;
}

.content-wrapper {
  position: relative;
  z-index: 1;
  padding: 60rpx;
}

.logo-area {
  text-align: center;
  margin-bottom: 60rpx;
  
  .logo {
    width: 180rpx;
    height: 180rpx;
    border-radius: 40rpx;
    box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.2);
    margin-bottom: 30rpx;
  }
  
  .text-area {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .app-name {
    font-size: 56rpx;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 4rpx;
    margin-bottom: 10rpx;
    text-shadow: 0 4rpx 10rpx rgba(0,0,0,0.1);
  }

  .app-slogan {
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.9);
    letter-spacing: 8rpx;
    font-weight: 300;
  }
}

.form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  border-radius: 40rpx;
  padding: 60rpx 50rpx;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.15);
}

.form-header {
  margin-bottom: 50rpx;
  text-align: center;
  .welcome-text {
    font-size: 36rpx;
    font-weight: 700;
    color: $text-main;
  }
}

.input-group {
  background: #F3F4F6;
  border-radius: 20rpx;
  padding: 24rpx 30rpx;
  margin-bottom: 32rpx;
  display: flex;
  align-items: center;
  transition: all 0.3s;
  border: 2rpx solid transparent;
  
  &:focus-within {
    background: #FFFFFF;
    border-color: $primary;
    box-shadow: 0 0 0 4rpx rgba(16, 185, 129, 0.1);
  }

  .input-icon-wrapper {
    margin-right: 20rpx;
    font-size: 36rpx;
    opacity: 0.6;
  }

  .input {
    flex: 1;
    font-size: 30rpx;
    color: $text-main;
    height: 48rpx; // Fix height for uniapp input
  }
  
  .input-placeholder {
    color: $text-sub;
  }
}

.btn-primary {
  margin-top: 60rpx;
  background: linear-gradient(135deg, $primary 0%, $primary-dark 100%);
  color: #fff;
  border-radius: 20rpx;
  font-size: 32rpx;
  font-weight: 600;
  padding: 10rpx 0; // vertical padding logic handles by height usually
  height: 96rpx;
  line-height: 96rpx;
  box-shadow: 0 10rpx 20rpx rgba(16, 185, 129, 0.3);
  border: none;
  
  &::after { border: none; }
}

.btn-hover {
  transform: translateY(2rpx);
  box-shadow: 0 6rpx 12rpx rgba(16, 185, 129, 0.2);
  opacity: 0.9;
}

.footer-actions {
  margin-top: 30rpx;
  text-align: center;
  .action-link {
    font-size: 26rpx;
    color: $text-sub;
  }
}

.footer {
  position: absolute;
  bottom: 40rpx;
  width: 100%;
  text-align: center;
  z-index: 1;
  .copyright {
    color: rgba(255, 255, 255, 0.6);
    font-size: 24rpx;
  }
}

// Animations
.animate-fade-in-down { animation: fadeInDown 0.8s ease-out; }
.animate-fade-in-up { animation: fadeInUp 0.8s ease-out 0.2s backwards; }
.animate-slide-up { animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.4s backwards; }

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-40rpx); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40rpx); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(100rpx); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
