<template>
  <view class="page">
    <view class="title" style="padding: 24rpx 24rpx 8rpx">统计报表</view>
    <view class="subtitle" style="padding: 0 24rpx 16rpx">后续可接入图表组件</view>
    <view class="card">
      <view>平均湿度：48.3%</view>
      <view>近 30 天病虫害：1 次</view>
      <view style="margin-top: 12rpx; color: #6b7280">TODO: 接入 eCharts 折线/柱状图</view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>
.page {
  padding: 16rpx 20rpx 40rpx;
}
</style>
