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
              <div style="font-size: 10px; color: red; margin-top: 5px;">{{ debugMsg }}</div>
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
          <div class="card-title">环境数据</div>
          <div class="sensor-grid" v-if="sensorList.length > 0">
            <div class="sensor-item" v-for="(sensor, index) in sensorList" :key="index">
              <div class="label">{{ sensor.label }}</div>
              <div class="value">{{ sensor.value }}</div>
              <div class="device-name" style="font-size: 10px; color: #ccc; margin-top: 2px;">{{ sensor.deviceName }}</div>
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
            <div class="advice-item warning">
              <el-icon><Warning /></el-icon>
              <span>检测到近期湿度较高，请注意防范茶饼病。</span>
            </div>
            <div class="advice-item info">
              <el-icon><InfoFilled /></el-icon>
              <span>适宜进行除草作业。</span>
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
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const gardenId = route.params.id
const garden = ref({})
const loading = ref(false)
const hasMap = ref(false)

// 天气数据
const weather = ref({
  temperature: '-',
  weather: '加载中',
  humidity: '-',
  windPower: '-'
})

// 传感器数据
const sensorList = ref([])

const fetchDetail = async () => {
  loading.value = true
  try {
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

const debugMsg = ref('')

const fetchWeather = (lat, lng) => {
  if (!window.AMap) {
    debugMsg.value = '等待地图加载...'
    setTimeout(() => fetchWeather(lat, lng), 500)
    return
  }
  
  debugMsg.value = '加载插件中...'
  window.AMap.plugin(['AMap.Geocoder', 'AMap.Weather'], function() {
    debugMsg.value = '插件加载完成，获取地址...'
    // 1. 先通过经纬度获取城市/区域编码
    const geocoder = new window.AMap.Geocoder()
    geocoder.getAddress([lng, lat], (status, result) => {
      console.log('Geocoder status:', status, result)
      if (status === 'complete' && result.regeocode) {
        const adcode = result.regeocode.addressComponent.adcode
        debugMsg.value = `获取地址成功: ${adcode}，查询天气...`
        queryWeather(adcode)
      } else {
        console.warn('Geocode failed:', result)
        debugMsg.value = `地址解析失败(${status})，尝试查询默认城市(杭州)天气...`
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
        if (adcode === '330100') {
             debugMsg.value = '已显示默认城市(杭州)天气 (定位解析失败)'
        } else {
             debugMsg.value = '天气更新成功'
        }
      } else {
        const errorInfo = err.info || '未知错误'
        if (errorInfo === 'USERKEY_PLAT_NOMATCH' || errorInfo === 'INVALID_USER_SCODE') {
            debugMsg.value = 'API Key 配置问题(缺安全密钥或类型错误)，已切换模拟数据'
            weather.value = {
              temperature: '26',
              weather: '晴',
              humidity: '45',
              windPower: '3'
            }
        } else {
            debugMsg.value = '天气查询失败: ' + errorInfo
        }
      }
    })
}

const fetchGardenDevices = async () => {
  try {
    // 获取该茶园下的所有设备
    const res = await getDeviceList({ garden_id: gardenId, size: 100 })
    const devices = res.list || []
    
    const allSensors = []
    
    // 并行获取每个设备的最新遥测数据
    const promises = devices.map(async (device) => {
      try {
        const telemetry = await getLatestTelemetry(device.id)
        // 解析传感器配置，获取单位和名称
        let config = {}
        try {
            if (device.sensor_config) {
                config = JSON.parse(device.sensor_config)
            }
        } catch (e) {}

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

        for (const [key, value] of Object.entries(latestData)) {
            // 跳过忽略的键
            if (config.__ignored && config.__ignored.includes(key)) continue
            if (key === 'ts') continue // 跳过时间戳

            const sensorConf = config[key] || {}
            const name = sensorConf.name || key
            const unit = sensorConf.unit || ''
            
            allSensors.push({
                label: name,
                value: value + (unit ? ' ' + unit : ''),
                deviceId: device.id,
                deviceName: device.name
            })
        }
      } catch (e) {
        console.error(`Failed to fetch telemetry for device ${device.id}`, e)
      }
    })
    
    await Promise.all(promises)
    sensorList.value = allSensors
  } catch (error) {
    console.error(error)
  }
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

onMounted(() => {
  fetchDetail()
})
</script>

<style scoped>
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
.sensor-item { background: #f9fafb; padding: 16px; border-radius: 8px; text-align: center; }
.sensor-item .label { font-size: 12px; color: #909399; margin-bottom: 4px; }
.sensor-item .value { font-size: 18px; font-weight: 600; color: #1f2a44; }

.ai-advice .advice-item { display: flex; align-items: flex-start; gap: 8px; padding: 12px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; line-height: 1.5; }
.advice-item.warning { background: #fdf6ec; color: #e6a23c; }
.advice-item.info { background: #f4f4f5; color: #909399; }
</style>