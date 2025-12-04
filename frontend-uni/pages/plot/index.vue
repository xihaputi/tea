<template>
  <view class="page-container">
    <!-- 顶部大图 Header -->
    <view class="hero-header" v-if="garden.name">
      <image class="hero-bg" :src="gardenImage" mode="aspectFill"></image>
      <view class="hero-overlay">
        <view class="hero-content">
          <view class="hero-top">
            <text class="hero-title">{{ garden.name }}</text>
            <view class="tag" :class="gardenStatusClass">{{ gardenStatusText }}</view>
          </view>
          <view class="hero-info">
             <text class="info-text">{{ garden.company || '未归属公司' }}</text>
             <text class="info-text" v-if="garden.manager"> | 负责人: {{ garden.manager }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 内容区域 -->
    <view class="content-wrapper">
        
        <!-- 1. 位置与天气卡片 -->
        <view class="card weather-card">
            <view class="card-header-sm">
                <text class="card-title-sm">📍 茶园位置与天气</text>
            </view>
            <view class="weather-body">
                <view class="location-row">
                    <text class="address-text">{{ garden.address || '地址未配置' }}</text>
                </view>
                <view class="weather-row">
                    <view class="weather-main">
                        <text class="temp">{{ weather.temperature }}°C</text>
                        <text class="weather-desc">{{ weather.weather }}</text>
                    </view>
                    <view class="weather-details">
                        <view class="detail-item">
                            <text class="label">湿度</text>
                            <text class="val">{{ weather.humidity }}%</text>
                        </view>
                        <view class="detail-item">
                            <text class="label">风力</text>
                            <text class="val">{{ weather.windPower }}级</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <!-- 2. 环境监测数据 (聚合) -->
        <view class="card sensor-card">
            <view class="card-header-sm">
                <text class="card-title-sm">🌱 环境监测</text>
                <text class="update-time" v-if="lastUpdated">更新于 {{ lastUpdated }}</text>
            </view>
            <view class="sensor-grid" v-if="sensorList.length > 0">
                <view class="sensor-item" v-for="(item, index) in sensorList" :key="index">
                    <text class="sensor-label">{{ item.label }}</text>
                    <text class="sensor-value">{{ item.value }}</text>
                    <text class="sensor-device">{{ item.deviceName }}</text>
                </view>
            </view>
            <view class="empty-sensor" v-else>
                <text>暂无环境数据</text>
            </view>
        </view>

        <!-- 3. AI 农事建议 -->
        <view class="card advice-card">
            <view class="card-header-sm">
                <text class="card-title-sm">🤖 AI 农事建议</text>
            </view>
            <view class="advice-list">
                <view class="advice-item" v-for="(item, index) in aiAdvice" :key="index" :class="item.type">
                    <text class="advice-icon">{{ item.type === 'warning' ? '⚠️' : '💡' }}</text>
                    <text class="advice-text">{{ item.text }}</text>
                </view>
            </view>
        </view>

        <!-- 4. 设备列表 -->
        <view class="section-header">
          <text class="title-md">设备列表</text>
          <text class="text-sub">共 {{ devices.length }} 台</text>
        </view>

        <view class="device-list">
          <view v-for="device in devices" :key="device.id" class="card device-card" @click="goDeviceDetail(device.id)">
            <view class="card-header">
              <view class="header-left">
                <text class="card-title">{{ device.name }}</text>
                <!-- <text class="sn-tag">SN: {{ device.sn }}</text> -->
              </view>
              <text class="status-text" :class="deviceStatusClass(device.status)">
                ● {{ deviceStatusText(device.status) }}
              </text>
            </view>

            <view class="card-body">
              <view class="info-row">
                <text class="label">最后在线：</text>
                <text class="value">{{ formatTime(device.last_time) }}</text>
              </view>
              <view class="info-row">
                <text class="label">序列号：</text>
                <text class="value">{{ device.sn }}</text>
              </view>
            </view>
            
            <!-- 简单的操作栏 -->
            <view class="card-footer-simple">
                <text class="arrow-text">查看详情 ></text>
            </view>
          </view>
        </view>
        
        <view v-if="devices.length === 0 && !loading" class="empty-state">
          <image src="/static/empty.png" mode="aspectFit" class="empty-img"></image>
          <text class="empty-text">该茶园暂无设备</text>
        </view>

    </view>
  </view>
</template>

<script>
import { getGardenDetail, getGardenDevices } from '@/api/garden.js';
import { getLatestTelemetry } from '@/api/device.js';

export default {
  data() {
    return {
      gardenId: null,
      garden: {},
      devices: [],
      loading: false,
      lastUpdated: '',
      
      // 模拟天气数据 (因为没有真实API)
      weather: {
          temperature: '24',
          weather: '多云',
          humidity: '65',
          windPower: '2'
      },
      
      sensorList: [],
      aiAdvice: [
          { type: 'info', text: '正在分析环境数据...' }
      ]
    };
  },
  computed: {
    gardenImage() {
      return this.garden.image_path ? (this.$baseUrl + this.garden.image_path) : '/static/garden_bg.png';
    },
    gardenStatusText() {
      const status = this.garden.status || 'normal';
      return status === 'normal' ? '正常运行' : '需关注';
    },
    gardenStatusClass() {
      const status = this.garden.status || 'normal';
      return status === 'normal' ? 'tag-primary' : 'tag-warn';
    }
  },
  onLoad(options) {
    if (options.garden_id) {
      this.gardenId = options.garden_id;
      this.loadData();
    }
  },
  onPullDownRefresh() {
      this.loadData().then(() => {
          uni.stopPullDownRefresh();
      });
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        // 1. 获取基本信息和设备列表
        const [garden, devices] = await Promise.all([
          getGardenDetail(this.gardenId),
          getGardenDevices(this.gardenId)
        ]);
        this.garden = garden;
        this.devices = devices;
        
        uni.setNavigationBarTitle({ title: garden.name });
        
        // 2. 获取传感器数据
        await this.fetchSensorData(devices);
        
      } catch (e) {
        console.error(e);
        uni.showToast({ title: '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    
    async fetchSensorData(devices) {
        const allSensors = [];
        
        const promises = devices.map(async (device) => {
            try {
                const telemetry = await getLatestTelemetry(device.id);
                
                // 解析配置
                let config = {};
                try {
                    if (device.sensor_config) {
                        config = JSON.parse(device.sensor_config);
                    }
                } catch(e) {}
                
                // 处理遥测数据
                const latestData = {};
                if (Array.isArray(telemetry)) {
                    telemetry.forEach(item => {
                        if (!latestData[item.key]) latestData[item.key] = item.value;
                    });
                }
                
                for (const [key, value] of Object.entries(latestData)) {
                    if (key === 'ts') continue;
                    // 简单过滤一些非环境数据
                    if (['battery', 'signal', 'version'].includes(key)) continue;
                    
                    const sensorConf = config[key] || {};
                    const name = sensorConf.name || this.formatKeyName(key);
                    const unit = sensorConf.unit || this.guessUnit(key);
                    
                    allSensors.push({
                        label: name,
                        value: value + unit,
                        rawVal: parseFloat(value), // 用于AI分析
                        key: key,
                        deviceName: device.name
                    });
                }
            } catch (e) {
                console.error(`Device ${device.id} telemetry error`, e);
            }
        });
        
        await Promise.all(promises);
        this.sensorList = allSensors;
        this.lastUpdated = new Date().toLocaleTimeString();
        this.generateAiAdvice(allSensors);
    },
    
    formatKeyName(key) {
        const map = {
            'temperature': '温度',
            'humidity': '湿度',
            'soil_moisture': '土壤湿度',
            'light': '光照',
            'co2': 'CO2浓度'
        };
        return map[key] || key;
    },
    
    guessUnit(key) {
        if (key.includes('temp')) return '℃';
        if (key.includes('humidity') || key.includes('moisture')) return '%';
        if (key.includes('light')) return 'Lux';
        return '';
    },
    
    generateAiAdvice(sensors) {
        const advice = [];
        
        // 简单的规则引擎
        const temp = sensors.find(s => s.key.includes('temp'));
        const humidity = sensors.find(s => s.key.includes('humidity'));
        const soil = sensors.find(s => s.key.includes('soil'));
        
        if (temp) {
            if (temp.rawVal > 30) advice.push({ type: 'warning', text: `气温较高(${temp.value})，注意茶树防晒。` });
            else if (temp.rawVal < 5) advice.push({ type: 'warning', text: `气温较低(${temp.value})，注意防冻。` });
        }
        
        if (soil) {
            if (soil.rawVal < 30) advice.push({ type: 'warning', text: `土壤较干(${soil.value})，建议灌溉。` });
        }
        
        if (advice.length === 0) {
            advice.push({ type: 'info', text: '当前环境适宜，茶树生长状况良好。' });
            advice.push({ type: 'info', text: '建议进行常规巡园检查。' });
        }
        
        this.aiAdvice = advice;
    },

    deviceStatusText(status) {
      return status === 'online' ? '在线' : '离线';
    },
    deviceStatusClass(status) {
      return status === 'online' ? 'text-primary' : 'text-sub';
    },
    formatTime(time) {
      if (!time) return '-';
      return new Date(time).toLocaleString();
    },
    goDeviceDetail(id) {
      uni.showToast({ title: '设备详情开发中', icon: 'none' });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page-container {
  padding-bottom: 40rpx;
  background-color: #F5F7FA;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden; /* 防止水平滚动 */
  box-sizing: border-box;
}

/* Hero Header */
.hero-header {
  position: relative;
  height: 560rpx; /* 进一步增加高度 */
  width: 100%;
}

.hero-bg {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 加深遮罩颜色以确保文字可见 */
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.8));
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中内容，避免被底部卡片遮挡 */
  padding: 0 32rpx 60rpx 32rpx; /* 调整内边距 */
}

.hero-content {
  color: #fff;
  z-index: 1;
}

.hero-top {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 16rpx;
}

.hero-title {
  font-size: 48rpx; /* 加大标题 */
  font-weight: 700;
  text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.5);
}

.hero-info {
    font-size: 28rpx;
    opacity: 0.95;
    text-shadow: 0 1rpx 2rpx rgba(0,0,0,0.5);
}

.content-wrapper {
    padding: 0 24rpx;
    margin-top: -80rpx; /* 让卡片上浮 */
    position: relative;
    z-index: 10;
    width: 100%;
    box-sizing: border-box; /* 确保 padding 不会撑大宽度 */
}

.card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
  width: 100%;
  box-sizing: border-box;
}

.card-header-sm {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
    border-bottom: 1rpx solid #f0f0f0;
    padding-bottom: 16rpx;
}

.card-title-sm {
    font-size: 30rpx;
    font-weight: 600;
    color: #333;
}

.update-time {
    font-size: 22rpx;
    color: #999;
}

/* Weather Card */
.weather-body {
    padding: 10rpx 0;
}
.location-row {
    margin-bottom: 24rpx;
    display: flex;
    align-items: center;
    gap: 8rpx;
}
.address-text {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
    line-height: 1.4;
}
.weather-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.weather-main {
    display: flex;
    align-items: baseline;
    gap: 16rpx;
}
.temp {
    font-size: 64rpx;
    font-weight: 700;
    color: #333;
}
.weather-desc {
    font-size: 32rpx;
    color: #666;
}
.weather-details {
    display: flex;
    gap: 30rpx;
}
.detail-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.detail-item .label {
    font-size: 22rpx;
    color: #999;
}
.detail-item .val {
    font-size: 28rpx;
    font-weight: 600;
    color: #333;
}

/* Sensor Grid */
.sensor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20rpx;
}
.sensor-item {
    background: #F9FAFB;
    padding: 20rpx;
    border-radius: 12rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
.sensor-label {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 8rpx;
}
.sensor-value {
    font-size: 36rpx;
    font-weight: 700;
    color: $primary;
    margin-bottom: 8rpx;
}
.sensor-device {
    font-size: 20rpx;
    color: #999;
}
.empty-sensor {
    text-align: center;
    color: #999;
    padding: 20rpx;
    font-size: 26rpx;
}

/* Advice */
.advice-list {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
}
.advice-item {
    display: flex;
    align-items: flex-start;
    gap: 16rpx;
    padding: 16rpx;
    border-radius: 12rpx;
    font-size: 26rpx;
    line-height: 1.5;
}
.advice-item.warning {
    background: #FFF7E6;
    color: #FA8C16;
}
.advice-item.info {
    background: #F0F9FF;
    color: #1890FF;
}

/* Device List */
.section-header {
  padding: 0 8rpx;
  margin-bottom: 20rpx;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.title-md {
    font-size: 32rpx;
    font-weight: 600;
    color: #333;
}
.text-sub {
    font-size: 24rpx;
    color: #999;
}

.device-card {
    padding: 0;
    overflow: hidden;
}
.card-header {
  padding: 24rpx;
  border-bottom: 1rpx solid #F3F4F6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #333;
}
.status-text {
  font-size: 24rpx;
  &.text-primary { color: $primary; }
  &.text-sub { color: $text-sub; }
}
.card-body {
  padding: 24rpx;
}
.info-row {
  display: flex;
  margin-bottom: 12rpx;
  font-size: 26rpx;
  &:last-child { margin-bottom: 0; }
}
.label {
  color: #999;
  width: 140rpx;
}
.value {
  color: #333;
  flex: 1;
}
.card-footer-simple {
    padding: 16rpx 24rpx;
    background: #F9FAFB;
    text-align: right;
}
.arrow-text {
    font-size: 24rpx;
    color: #999;
}

.empty-state {
  padding: 80rpx 0;
  text-align: center;
}
.empty-img {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 24rpx;
}
.empty-text {
  color: #999;
  font-size: 28rpx;
}
</style>
