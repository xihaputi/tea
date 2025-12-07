<template>
  <view class="login-container">
    <view class="logo-area">
      <image src="/static/logo.png" mode="aspectFit" class="logo"></image>
      <text class="app-name">茶园智慧管理平台</text>
      <text class="app-slogan">科技赋能 · 智慧种茶</text>
    </view>

    <view class="form-area card">
      <view class="form-title">欢迎登录</view>
      
      <view class="input-group">
        <text class="label">账号</text>
        <input class="input" v-model="form.username" placeholder="请输入用户名" />
      </view>
      
      <view class="input-group">
        <text class="label">密码</text>
        <input class="input" v-model="form.password" password placeholder="请输入密码" />
      </view>

      <button class="btn-primary" @click="handleLogin" :loading="loading">立即登录</button>
    </view>
    
    <view class="footer">
      <text class="copyright">© 2024 Tea Garden IoT</text>
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
        // Save token
        uni.setStorageSync('token', res.token);
        uni.setStorageSync('userInfo', res.userInfo); // Optional: save user info
        uni.setStorageSync('roles', res.userInfo.roles || []); // Save roles
        
        uni.showToast({ title: '登录成功', icon: 'success' });
        
        // Redirect to home dashboard
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
  background: linear-gradient(135deg, $primary-light 0%, #ffffff 100%);
  padding: 60rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-area {
  text-align: center;
  margin-bottom: 80rpx;
}

.logo {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 24rpx;
  border-radius: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(16, 185, 129, 0.2);
}

.app-name {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $primary-dark;
  margin-bottom: 12rpx;
}

.app-slogan {
  display: block;
  font-size: 28rpx;
  color: $text-sub;
  letter-spacing: 4rpx;
}

.form-area {
  padding: 48rpx;
}

.form-title {
  font-size: 36rpx;
  font-weight: 700;
  color: $text-main;
  margin-bottom: 48rpx;
  text-align: center;
}

.input-group {
  margin-bottom: 32rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: $text-main;
  font-weight: 600;
  margin-bottom: 16rpx;
}

.input {
  background: #F9FAFB;
  border: 2rpx solid #E5E7EB;
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 30rpx;
  color: $text-main;
  transition: all 0.2s;
  
  &:focus {
    border-color: $primary;
    background: #fff;
  }
}

.btn-primary {
  margin-top: 48rpx;
  width: 100%;
  font-size: 32rpx;
  padding: 28rpx;
}

.footer {
  margin-top: 80rpx;
  text-align: center;
}

.copyright {
  font-size: 24rpx;
  color: $text-sub;
  opacity: 0.6;
}
</style>
