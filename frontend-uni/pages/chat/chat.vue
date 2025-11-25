<template>
  <view class="page">
    <view class="title" style="padding: 24rpx 24rpx 8rpx">AI 茶农顾问</view>
    <view class="subtitle" style="padding: 0 24rpx 16rpx">提问即可获得回答（示例）</view>

    <view class="card" v-for="(msg, idx) in history" :key="idx">
      <view class="subtitle">{{ msg.role === 'user' ? '你' : 'AI' }}</view>
      <view>{{ msg.content }}</view>
    </view>

    <view class="card">
      <textarea v-model="question" placeholder="请输入问题" style="width: 100%; min-height: 140rpx" />
      <view class="btn-primary" style="margin-top: 12rpx" @click="ask" :disabled="loading">
        {{ loading ? '发送中...' : '发送' }}
      </view>
    </view>
  </view>
</template>

<script>
import { api } from '../../common/http.js';

export default {
  data() {
    return {
      question: '',
      history: [],
      loading: false,
    };
  },
  methods: {
    async ask() {
      if (!this.question) return;
      const userMessage = { role: 'user', content: this.question };
      this.history.push(userMessage);
      this.loading = true;
      try {
        const res = await api.post('/chat/ask', {
          question: this.question,
          history: this.history,
        });
        this.history.push({ role: 'assistant', content: res.answer });
        this.question = '';
      } catch (e) {
        this.history.push({ role: 'assistant', content: '请求失败，请检查后端服务。' });
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
</style>
