<template>
  <view class="page">
    <view class="title header">我的</view>

    <view class="card profile">
      <view class="avatar"></view>
      <view class="account-box">
        <text>{{ accountName }}</text>
      </view>
    </view>

    <view class="card actions">
      <button @click="switchAccount">切换账号</button>
      <button type="warn" @click="logout">退出登录</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      accountName: '账号名称',
    };
  },
  methods: {
    switchAccount() {
      uni.showToast({ title: '切换账号（占位）', icon: 'none' });
    },
    logout() {
      uni.showToast({ title: '退出登录（占位）', icon: 'none' });
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
.header {
  padding: 24rpx 24rpx 8rpx;
}
.profile {
  display: flex;
  align-items: center;
  gap: 24rpx;
}
.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  border: 2rpx solid #1f7a5a;
}
.account-box {
  flex: 1;
  padding: 16rpx;
  border: 2rpx solid #d1d5db;
  border-radius: 12rpx;
}
.actions {
  display: flex;
  gap: 20rpx;
  justify-content: space-between;
}
.actions button {
  flex: 1;
}
</style>
