<template>
  <view class="page-container chat-page">
    <view class="chat-list">
      <view class="system-msg">
        <text class="system-text">AI 茶农顾问为您服务，请提问</text>
      </view>
      
      <view v-for="(msg, idx) in history" :key="idx" class="msg-row" :class="msg.role === 'user' ? 'msg-right' : 'msg-left'">
        
        <!-- AI Avatar -->
        <view v-if="msg.role === 'assistant'" class="avatar ai-avatar">🤖</view>
        
        <view class="bubble" :class="msg.role === 'user' ? 'bubble-user' : 'bubble-ai'">
          <text class="msg-content">{{ msg.content }}</text>
        </view>
        
        <!-- User Avatar -->
        <view v-if="msg.role === 'user'" class="avatar user-avatar">👤</view>
      </view>
      
      <!-- Loading Indicator -->
      <view v-if="loading" class="msg-row msg-left">
        <view class="avatar ai-avatar">🤖</view>
        <view class="bubble bubble-ai">
          <text class="msg-content">思考中...</text>
        </view>
      </view>
      
      <!-- Spacer for bottom input -->
      <view style="height: 120rpx"></view>
    </view>

    <!-- Bottom Input Area -->
    <view class="input-area">
      <view class="input-box">
        <input class="chat-input" v-model="question" placeholder="请输入您的问题..." @confirm="ask" />
        <view class="send-btn" @click="ask" :class="{ disabled: !question || loading }">
          <text class="send-icon">↑</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { askChatbot, getLatestChat } from '@/api/chat.js';

export default {
  data() {
    return {
      question: '',
      history: [],
      sessionId: null,
      loading: false,
    };
  },
  onLoad() {
    this.loadHistory();
  },
  methods: {
    async loadHistory() {
      try {
        const res = await getLatestChat();
        if (res.session_id) {
          this.sessionId = res.session_id;
          this.history = res.history || [];
          this.scrollToBottom();
        }
      } catch (e) {
        console.error('Failed to load history', e);
      }
    },
    async ask() {
      if (!this.question || this.loading) return;
      
      const content = this.question;
      this.question = ''; // Clear immediately
      
      // Add user message
      this.history.push({ role: 'user', content });
      this.scrollToBottom();
      
      this.loading = true;
      try {
        const res = await askChatbot({
          question: content,
          history: this.history.map(m => ({ role: m.role, content: m.content })),
          session_id: this.sessionId
        });
        
        if (res.session_id) {
          this.sessionId = res.session_id;
        }
        
        this.history.push({ role: 'assistant', content: res.answer });
      } catch (e) {
        this.history.push({ role: 'assistant', content: '抱歉，我现在无法回答，请稍后再试。' });
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      setTimeout(() => {
        uni.pageScrollTo({ scrollTop: 99999, duration: 300 });
      }, 100);
    }
  },
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.chat-page {
  padding: 24rpx;
  background-color: $bg-page;
  min-height: 100vh;
}

.system-msg {
  text-align: center;
  margin: 24rpx 0;
}

.system-text {
  font-size: 24rpx;
  color: #9CA3AF;
  background: rgba(0,0,0,0.05);
  padding: 8rpx 24rpx;
  border-radius: 999rpx;
}

.msg-row {
  display: flex;
  margin-bottom: 32rpx;
  align-items: flex-start;
  
  &.msg-right {
    justify-content: flex-end;
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  flex-shrink: 0;
  
  &.ai-avatar {
    background: #E0E7FF;
    margin-right: 16rpx;
  }
  
  &.user-avatar {
    background: $primary-light;
    margin-left: 16rpx;
  }
}

.bubble {
  max-width: 60%;
  padding: 24rpx;
  border-radius: 20rpx;
  font-size: 30rpx;
  line-height: 1.5;
  position: relative;
  
  &.bubble-ai {
    background: #fff;
    color: $text-main;
    border-top-left-radius: 4rpx;
    box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.05);
  }
  
  &.bubble-user {
    background: $primary;
    color: #fff;
    border-top-right-radius: 4rpx;
    box-shadow: 0 2rpx 8rpx rgba(16, 185, 129, 0.2);
  }
}

/* Bottom Input Area */
.input-area {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #fff;
  padding: 24rpx;
  padding-bottom: calc(24rpx + constant(safe-area-inset-bottom));
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  box-shadow: 0 -4rpx 16rpx rgba(0,0,0,0.05);
}

.input-box {
  display: flex;
  align-items: center;
  background: #F3F4F6;
  border-radius: 40rpx;
  padding: 12rpx 12rpx 12rpx 32rpx;
}

.chat-input {
  flex: 1;
  height: 72rpx;
  font-size: 30rpx;
  color: $text-main;
}

.send-btn {
  width: 72rpx;
  height: 72rpx;
  background: $primary;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 16rpx;
  transition: all 0.2s;
  
  &.disabled {
    background: #D1D5DB;
    opacity: 0.8;
  }
  
  &:active:not(.disabled) {
    transform: scale(0.9);
  }
}

.send-icon {
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
}
</style>
