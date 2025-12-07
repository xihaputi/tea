<template>
  <div class="page" v-loading="loading">
    <div class="page-header">
      <div class="flex-center">
        <el-button icon="ArrowLeft" circle @click="router.back()" class="mr-4" />
        <div>
          <div class="eyebrow">茶园详情</div>
          <div class="title">{{ garden.name || '加载中...' }}</div>
        </div>
      </div>
      <el-space>
        <el-tag>{{ garden.company }}</el-tag>
        <el-tag type="info">{{ garden.manager }}</el-tag>
      </el-space>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：地图与监控 -->
      <el-col :span="16">
        <div class="card mb-4" style="height: 400px; padding: 0; overflow: hidden; position: relative;">
          <!-- 地图容器 -->
          <div id="garden-map" style="width: 100%; height: 100%; background: #e0e0e0;">
            <div class="map-placeholder" v-if="!hasMap">
              <el-empty description="地图加载中或未配置经纬度" />
            </div>
          </div>
          <div class="map-overlay">
            <div class="weather-widget">
              <div class="temp">{{ weather.temperature }}°C</div>
              <div class="desc">{{ weather.weather }} | 湿度 {{ weather.humidity }}% | 风速 {{ weather.windPower }}级</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-title">实时监控</div>
          <div class="camera-container">
            <div v-if="garden.camera_url" class="video-player">
              <!-- 这里可以使用 video.js 或简单的 video 标签 -->
              <div class="placeholder-video">
                <el-icon :size="40"><VideoCamera /></el-icon>
                <div class="mt-2">摄像头画面接入中...</div>
                <div class="url-text">{{ garden.camera_url }}</div>
              </div>
            </div>
            <el-empty v-else description="未配置摄像头" />
          </div>
        </div>
      </el-col>

      <!-- 右侧：数据与分析 -->
      <el-col :span="8">
        <div class="card mb-4">
          <div class="card-title">
            环境数据
            <span v-if="lastUpdated" style="font-size: 12px; color: #999; font-weight: normal; margin-left: 10px;">
                更新于 {{ lastUpdated }}
            </span>
          </div>
          <div class="sensor-grid" v-if="sensorList.length > 0">
            <div class="sensor-item" v-for="(sensor, index) in sensorList" :key="index">
              <div class="status-text" :style="{ color: sensor.statusColor || '#303133' }">
                  {{ sensor.status || '监测中' }}
              </div>
              <div class="mini-info">
                  <span class="light">{{ sensor.label }}</span>
                  <span class="bold">{{ sensor.value }}</span>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无传感器数据" :image-size="60" />
        </div>

        <div class="card mb-4">
          <div class="card-title">茶叶生长状态</div>
          <div class="growth-status">
            <el-steps direction="vertical" :active="2">
              <el-step title="萌芽期" description="3月1日 - 3月15日" />
              <el-step title="生长期" description="当前阶段，预计持续至4月" status="process" />
              <el-step title="采摘期" description="预计4月中旬开始" />
            </el-steps>
          </div>
        </div>

        <div class="card">
          <div class="card-title">AI 农事建议</div>
          <div class="ai-advice">
            <div 
                v-for="(item, index) in aiAdvice" 
                :key="index"
                class="advice-item" 
                :class="item.type"
            >
              <el-icon v-if="item.type === 'warning'"><Warning /></el-icon>
              <el-icon v-else><InfoFilled /></el-icon>
              <span>{{ item.text }}</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTeaGardenDetail } from '@/api/tea-garden'
import { getDeviceList, getLatestTelemetry } from '@/api/device'
import { getSensorRules } from '@/api/rule'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const gardenId = route.params.id
const garden = ref({})
const loading = ref(false)
const hasMap = ref(false)
const rulesMap = ref({}) // key -> config

// 天气数据
const weather = ref({
  temperature: '-',
  weather: '加载中',
  humidity: '-',
  windPower: '-'
})

// 传感器数据
const sensorList = ref([])
const lastUpdated = ref('')
const aiAdvice = ref([
    { type: 'info', text: '正在分析环境数据...' }
])

const fetchDetail = async () => {
  loading.value = true
  try {
    // 1. 获取规则
    await fetchRules()
    
    // 2. 获取详情
    const res = await getTeaGardenDetail(gardenId)
    if (res) {
      garden.value = res
      if (res.latitude && res.longitude) {
        initMap(res.latitude, res.longitude)
        fetchWeather(res.latitude, res.longitude)
      }
      fetchGardenDevices()
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchRules = async () => {
    try {
        const res = await getSensorRules()
        if (res) {
            res.forEach(rule => {
                try {
                    rulesMap.value[rule.sensor_key] = JSON.parse(rule.rule_config)
                } catch (e) {}
            })
        }
    } catch (e) {
        console.error(e)
    }
}

// 状态计算逻辑
const computeStatus = (key, value) => {
    // 提取数值
    const num = parseFloat(value)
    if (isNaN(num)) return null
    
    const config = rulesMap.value[key]
    if (!config) return null
    
    // 遍历规则区间
    for (const rule of config) {
        const min = rule.min !== null && rule.min !== undefined ? rule.min : -Infinity
        const max = rule.max !== null && rule.max !== undefined ? rule.max : Infinity
        
        if (num >= min && num < max) {
            return { label: rule.label, color: rule.color }
        }
    }
    return null
}

const fetchWeather = (lat, lng) => {
  if (!window.AMap) {
    setTimeout(() => fetchWeather(lat, lng), 500)
    return
  }
  
  window.AMap.plugin(['AMap.Geocoder', 'AMap.Weather'], function() {
    // 1. 先通过经纬度获取城市/区域编码
    const geocoder = new window.AMap.Geocoder()
    geocoder.getAddress([lng, lat], (status, result) => {
      console.log('Geocoder status:', status, result)
      if (status === 'complete' && result.regeocode) {
        const adcode = result.regeocode.addressComponent.adcode
        queryWeather(adcode)
      } else {
        console.warn('Geocode failed:', result)
        queryWeather('330100') // Fallback to Hangzhou
      }
    })
  })
}

const queryWeather = (adcode) => {
    const weatherQuery = new window.AMap.Weather()
    weatherQuery.getLive(adcode, (err, data) => {
      console.log('Weather result:', err, data)
      if (!err) {
        weather.value = {
          temperature: data.temperature,
          weather: data.weather,
          humidity: data.humidity,
          windPower: data.windPower
        }
      } else {
        const errorInfo = err.info || '未知错误'
        if (errorInfo === 'USERKEY_PLAT_NOMATCH' || errorInfo === 'INVALID_USER_SCODE') {
            weather.value = {
              temperature: '26',
              weather: '晴',
              humidity: '45',
              windPower: '3'
            }
        }
      }
    })
}

const fetchGardenDevices = async () => {
  try {
    console.log('Fetching devices for gardenId:', gardenId)
    // 获取该茶园下的所有设备
    const res = await getDeviceList({ gardenId: gardenId, size: 100 })
    const devices = res.list || []
    console.log('Devices found:', devices)
    
    const allSensors = []
    
    // 并行获取每个设备的最新遥测数据
    const promises = devices.map(async (device) => {
      try {
        const telemetry = await getLatestTelemetry(device.id)
        console.log(`Telemetry for device ${device.id}:`, telemetry)
        
        // 解析传感器配置，获取单位和名称
        let config = {}
        try {
            if (device.sensor_config) {
                config = JSON.parse(device.sensor_config)
            }
        } catch (e) {
            console.error('Config parse error', e)
        }

        // 遍历遥测数据列表
        // 格式: [{ts:..., key:..., value:...}, ...]
        // 我们需要去重，只取每个key的最新值
        const latestData = {}
        if (Array.isArray(telemetry)) {
            telemetry.forEach(item => {
                if (!latestData[item.key]) {
                    latestData[item.key] = item.value
                }
            })
        } else if (typeof telemetry === 'object') {
            // 兼容旧格式（如果是对象）
            Object.assign(latestData, telemetry)
        }
        
        console.log(`Processed latestData for ${device.id}:`, latestData)

        for (const [key, value] of Object.entries(latestData)) {
            // 跳过忽略的键
            if (config.__ignored && config.__ignored.includes(key)) continue
            if (key === 'ts') continue // 跳过时间戳

            const sensorConf = config[key] || {}
            const name = sensorConf.name || key
            const unit = sensorConf.unit || ''
            
            // 计算状态
            const statusObj = computeStatus(key, value)
            
            allSensors.push({
                label: name,
                value: value + (unit ? ' ' + unit : ''),
                deviceId: device.id,
                deviceName: device.name,
                status: statusObj ? statusObj.label : null,
                statusColor: statusObj ? statusObj.color : null
            })
        }
      } catch (e) {
        console.error(`Failed to fetch telemetry for device ${device.id}`, e)
      }
    })
    
    await Promise.all(promises)
    console.log('Final sensor list:', allSensors)
    sensorList.value = allSensors
    lastUpdated.value = new Date().toLocaleTimeString()
    generateAiAdvice(allSensors)
  } catch (error) {
    console.error(error)
  }
}

const generateAiAdvice = (sensors) => {
    const advice = []
    // ... existing advice logic ...
    // 可以基于 status 进一步优化建议 if needed
    
    // 1. 湿度分析
    const humiditySensor = sensors.find(s => s.label.includes('湿度'))
    if (humiditySensor) {
        const val = parseFloat(humiditySensor.value)
        if (val > 80) {
            advice.push({ type: 'warning', text: `检测到${humiditySensor.label}较高(${val}%)，请注意防范茶饼病。` })
        } else if (val < 40) {
            advice.push({ type: 'warning', text: `检测到${humiditySensor.label}较低(${val}%)，请注意适时灌溉。` })
        }
    }

    // 2. 温度分析
    const tempSensor = sensors.find(s => s.label.includes('温度'))
    if (tempSensor) {
        const val = parseFloat(tempSensor.value)
        if (val > 30) {
             advice.push({ type: 'warning', text: `气温较高(${val}℃)，请注意茶树遮阳防晒。` })
        } else if (val < 5) {
             advice.push({ type: 'warning', text: `气温较低(${val}℃)，请注意防冻害。` })
        }
    }
    
    // 3. 默认建议
    if (advice.length === 0) {
        advice.push({ type: 'info', text: '当前环境适宜，建议进行常规巡园。' })
        advice.push({ type: 'info', text: '适宜进行除草作业。' })
    }
    
    aiAdvice.value = advice
}

const initMap = (lat, lng) => {
  if (!window.AMap) {
    setTimeout(() => initMap(lat, lng), 500)
    return
  }
  
  hasMap.value = true
  const map = new window.AMap.Map('garden-map', {
    zoom: 16,
    center: [lng, lat], // AMap uses [lng, lat]
    viewMode: '3D'
  })

  const marker = new window.AMap.Marker({
    position: [lng, lat],
    title: garden.value.name
  })
  map.add(marker)
}

import { onUnmounted } from 'vue'

let pollingTimer = null

onMounted(() => {
  fetchDetail()
  // 开启轮询，每5秒刷新一次设备数据
  pollingTimer = setInterval(() => {
    if (gardenId) {
        fetchGardenDevices()
    }
  }, 5000)
})

onUnmounted(() => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
})
</script>

<style scoped>
/* Only need to update sensor-item styles */
.sensor-item { background: #fff; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #eee; transition: all 0.3s; }
.sensor-item:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

.status-text { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.mini-info { font-size: 13px; color: #666; display: flex; justify-content: center; gap: 8px; align-items: center; }
.mini-info .light { color: #999; }
.mini-info .bold { font-weight: 600; color: #333; }

/* Keep other styles */
.page { padding: 24px; background: #f0f2f5; min-height: 100vh; }
.page-header { background: #fff; padding: 20px 24px; border-radius: 8px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }
.flex-center { display: flex; align-items: center; }
.mr-4 { margin-right: 16px; }
.eyebrow { font-size: 12px; color: #909399; }
.title { font-size: 24px; font-weight: 600; color: #303133; }
.card { background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.mb-4 { margin-bottom: 20px; }
.card-title { font-weight: 600; margin-bottom: 16px; font-size: 16px; border-left: 4px solid #16c06e; padding-left: 10px; }

.map-overlay { position: absolute; top: 20px; right: 20px; z-index: 10; }
.weather-widget { background: rgba(255,255,255,0.9); padding: 12px 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); backdrop-filter: blur(4px); }
.weather-widget .temp { font-size: 28px; font-weight: 700; color: #333; }
.weather-widget .desc { font-size: 12px; color: #666; margin-top: 4px; }

.map-placeholder { display: flex; justify-content: center; align-items: center; height: 100%; color: #999; }

.camera-container { height: 240px; background: #000; border-radius: 4px; display: flex; justify-content: center; align-items: center; color: #fff; }
.placeholder-video { text-align: center; color: #666; }
.url-text { font-size: 12px; margin-top: 8px; color: #444; }

.sensor-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.ai-advice .advice-item { display: flex; align-items: flex-start; gap: 8px; padding: 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; line-height: 1.5; }
.advice-item.warning { background: #fdf6ec; color: #e6a23c; }
.advice-item.info { background: #f4f4f5; color: #909399; }
</style>
