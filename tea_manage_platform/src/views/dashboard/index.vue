<template>
  <div class="dashboard-container">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="24">
      <el-col :span="6" v-for="(item, index) in statCards" :key="index">
        <el-card shadow="hover" class="stat-card" :class="'stat-card-' + index">
          <div class="stat-content">
            <div class="stat-icon-wrapper">
              <el-icon class="stat-icon"><component :is="item.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-label">{{ item.label }}</div>
            </div>
          </div>
          <div class="card-bg-decoration"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 中间区域：告警列表 + 趋势缩略图 -->
    <el-row :gutter="24" class="mt-6">
      <!-- 告警列表 -->
      <el-col :span="14">
        <el-card shadow="hover" class="alarm-list-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">
                <el-icon class="mr-2 text-red-500"><Warning /></el-icon>实时告警
              </span>
              <el-button type="primary" link @click="router.push('/alarm/index')">查看全部</el-button>
            </div>
          </template>
          <div class="alarm-list-container">
            <el-table :data="alarmList" style="width: 100%" :show-header="true" size="small">
              <el-table-column prop="created_at" label="时间" width="160">
                <template #default="{ row }">
                  {{ formatTime(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column prop="gardenName" label="所属茶园" width="120" show-overflow-tooltip />
              <el-table-column prop="deviceName" label="设备" width="120" show-overflow-tooltip />
              <el-table-column prop="content" label="内容" show-overflow-tooltip>
                <template #default="{ row }">
                  <span class="text-red-500">{{ row.content }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      
      <!-- 趋势缩略图 -->
      <el-col :span="10">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">
                <el-icon class="mr-2"><TrendCharts /></el-icon>告警趋势
              </span>
            </div>
          </template>
          <div ref="lineChartRef" class="chart-container-mini"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 茶园概览卡片 -->
    <div class="section-title mt-8">
      <el-icon class="mr-2"><Collection /></el-icon>茶园概览
    </div>
    <el-row :gutter="24" class="mt-4">
      <el-col :span="6" v-for="garden in gardenList" :key="garden.id" class="mb-6">
        <el-card 
          shadow="hover" 
          class="garden-card" 
          :class="{ 'has-alarm': garden.alarmCount > 0 }"
        >
          <div class="garden-image-wrapper" @click="router.push(`/tea-garden/detail/${garden.id}`)">
            <img 
              :src="getGardenImage(garden)" 
              class="garden-image" 
              alt="Garden Image"
            />
            <div class="garden-status" :class="garden.status === 'active' ? 'status-active' : 'status-inactive'">
              {{ garden.status === 'active' ? '正常运营' : '维护中' }}
            </div>
            
            <!-- 封面上传按钮 (移到右上角，改为点击选择) -->
            <div class="card-actions" @click.stop>
                <el-button 
                    type="primary" 
                    circle 
                    size="small" 
                    :icon="Edit" 
                    class="action-btn"
                    @click="openImageSelector(garden)"
                />
            </div>
          </div>
          
          <div class="garden-info" @click="router.push(`/tea-garden/detail/${garden.id}`)">
            <h3 class="garden-name">
              {{ garden.name }}
              <el-tag v-if="garden.alarmCount > 0" type="danger" size="small" effect="dark" class="ml-2">
                {{ garden.alarmCount }} 告警
              </el-tag>
            </h3>
            <div class="garden-detail-row">
              <el-icon><Location /></el-icon>
              <span class="truncate">{{ garden.address || '暂无地址' }}</span>
            </div>
            <div class="garden-detail-row">
              <el-icon><User /></el-icon>
              <span>负责人: {{ garden.manager || '未设置' }}</span>
            </div>
            <div class="garden-stats-row">
              <div class="stat-mini">
                <span class="label">面积</span>
                <span class="value">{{ garden.area || 0 }} 亩</span>
              </div>
              <div class="stat-mini">
                <span class="label">设备</span>
                <span class="value">{{ garden.totalCount || 0 }} 台</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    
    <ImageSelector 
        v-model="showImageSelector"
        :current-image="currentEditGarden?.image_path"
        @select="handleImageSelect"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { getDashboardStats } from '@/api/dashboard'
import { getTeaGardenList, updateTeaGarden } from '@/api/tea-garden'
import { getAlarmList } from '@/api/alarm'
import { uploadFile } from '@/api/upload'
import { Collection, Cpu, Bell, User, TrendCharts, PieChart, Picture, Location, Warning, Camera, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import ImageSelector from '@/components/ImageSelector.vue'


const router = useRouter()

const stats = reactive({
  garden_count: 0,
  device_count: 0,
  device_online_count: 0,
  alarm_count: 0,
  user_count: 0,
  alarm_trend: []
})

const showImageSelector = ref(false)
const currentEditGarden = ref(null)

const gardenList = ref([])
const alarmList = ref([])

const statCards = computed(() => [
  { label: '茶园总数', value: stats.garden_count, icon: Collection },
  { label: '设备总数', value: stats.device_count, icon: Cpu },
  { label: '当前告警', value: stats.alarm_count, icon: Bell },
  { label: '用户总数', value: stats.user_count, icon: User },
])

const lineChartRef = ref(null)
let lineChart = null
let timer = null

// 默认茶园图片
const defaultImages = [
  'https://images.unsplash.com/photo-1586616801904-74d47e650d99?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1563822249548-9a72b6353cd1?q=80&w=600&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1597479715535-257a06626998?q=80&w=600&auto=format&fit=crop'
]

const getGardenImage = (garden) => {
  if (garden.image_path) {
    // 如果是后端返回的相对路径 (包括 /static/)，添加后端 API 前缀
    if (garden.image_path.startsWith('/')) {
      return import.meta.env.VITE_APP_BASE_API + garden.image_path
    }
    return garden.image_path
  }
  // 随机返回一个默认图片 (根据ID固定)
  return defaultImages[garden.id % defaultImages.length]
}

const formatTime = (time) => {
  return dayjs(time).format('MM-DD HH:mm')
}

const openImageSelector = (garden) => {
    currentEditGarden.value = garden
    showImageSelector.value = true
}

const handleImageSelect = async (url) => {
  if (!currentEditGarden.value) return
  
  try {
    const garden = currentEditGarden.value
    // 更新茶园信息
    await updateTeaGarden(garden.id, { image_path: url })
    garden.image_path = url
    ElMessage.success('封面更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
    console.error(error)
  }
}

const initCharts = () => {
  const isDark = document.documentElement.classList.contains('dark')
  const textColor = isDark ? '#ccc' : '#333'
  
  if (lineChartRef.value) {
    lineChart = echarts.init(lineChartRef.value)
    const dates = stats.alarm_trend.map(item => item.name)
    const values = stats.alarm_trend.map(item => item.value)
    
    lineChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates,
        axisLabel: { color: textColor, fontSize: 10 },
        axisTick: { show: false }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: textColor, fontSize: 10 },
        splitLine: { lineStyle: { color: isDark ? '#333' : '#eee' } }
      },
      series: [
        {
          name: '告警数量',
          type: 'line',
          smooth: true,
          showSymbol: false,
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(245, 108, 108, 0.5)' },
              { offset: 1, color: 'rgba(245, 108, 108, 0.0)' }
            ])
          },
          itemStyle: { color: '#f56c6c' },
          lineStyle: { width: 2 },
          data: values
        }
      ]
    })
  }
}

const fetchData = async () => {
  try {
    const [statsRes, gardenRes, alarmRes] = await Promise.all([
      getDashboardStats(),
      getTeaGardenList({ page: 1, size: 100 }),
      getAlarmList({ page: 1, size: 5, status: 'active' })
    ])
    Object.assign(stats, statsRes)
    gardenList.value = gardenRes.list
    alarmList.value = alarmRes.list
    nextTick(() => {
      initCharts()
    })
  } catch (error) {
    console.error(error)
  }
}

const handleResize = () => {
  lineChart && lineChart.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
  // 自动刷新 (30秒) / Auto refresh (30s)
  timer = setInterval(fetchData, 30000)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  lineChart && lineChart.dispose()
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
  background-color: transparent;
}

/* 统计卡片样式 */
.stat-card {
  border: none;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  cursor: default;
}
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
.stat-content {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 2;
  padding: 10px 0;
}
.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 28px;
  color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
/* 卡片配色 */
.stat-card-0 .stat-icon-wrapper { background: linear-gradient(135deg, #409eff, #36cfc9); }
.stat-card-1 .stat-icon-wrapper { background: linear-gradient(135deg, #67c23a, #95d475); }
.stat-card-2 .stat-icon-wrapper { background: linear-gradient(135deg, #f56c6c, #f89898); }
.stat-card-3 .stat-icon-wrapper { background: linear-gradient(135deg, #909399, #b1b3b8); }

/* 图表和列表卡片 */
.chart-card, .alarm-list-card {
  border-radius: 12px;
  border: none;
  height: 100%;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
  font-size: 16px;
}
.header-title {
  display: flex;
  align-items: center;
}
.chart-container-mini {
  height: 200px;
}
.alarm-list-container {
  height: 200px;
  overflow-y: auto;
}

/* 茶园概览 */
.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #303133;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding-left: 8px;
  border-left: 4px solid #13c2c2;
}
.garden-card {
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
  padding: 0;
  position: relative;
}
.garden-card :deep(.el-card__body) {
  padding: 0;
}
.garden-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
/* 告警红框效果 */
.garden-card.has-alarm {
  border: 2px solid #f56c6c;
  box-shadow: 0 0 10px rgba(245, 108, 108, 0.2);
}

.garden-image-wrapper {
  height: 160px;
  position: relative;
  overflow: hidden;
}
.garden-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}
.garden-card:hover .garden-image {
  transform: scale(1.05);
}

.garden-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  color: #fff;
  font-weight: 500;
  z-index: 2;
}
.status-active { background: rgba(103, 194, 58, 0.9); }
.status-inactive { background: rgba(144, 147, 153, 0.9); }

/* 上传/编辑按钮 */
.card-actions {
  position: absolute;
  top: 12px;
  right: 12px; /* Next to status which is 12px right? Wait, status is absolute too. */
  z-index: 5;
  /* status is at right: 12px as well. We need to move one. 
     Let's put the button strictly at top-right, and move status down or left.
     Or put button at top-LEFT? The user said "top right".
     Status is also "active" / "maintenance". 
     Let's put the button at top-right (z-index higher) and move status to top-left?
     Or put button below status? 
     Let's move status to top-left.
  */
}
.garden-status {
    right: auto;
    left: 12px;
}

.action-btn {
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.garden-info {
  padding: 16px;
}
.garden-name {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.garden-detail-row {
  display: flex;
  align-items: center;
  color: #606266;
  font-size: 13px;
  margin-bottom: 8px;
}
.garden-detail-row .el-icon {
  margin-right: 6px;
  color: #909399;
}
.garden-stats-row {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}
.stat-mini {
  display: flex;
  flex-direction: column;
}
.stat-mini .label {
  font-size: 12px;
  color: #909399;
}
.stat-mini .value {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-top: 2px;
}

.mt-6 { margin-top: 24px; }
.mt-8 { margin-top: 32px; }
.mt-4 { margin-top: 16px; }
.mb-6 { margin-bottom: 24px; }
.mr-2 { margin-right: 8px; }
.ml-2 { margin-left: 8px; }
.text-red-500 { color: #f56c6c; }
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 暗黑模式适配 */
:global(.dark) .stat-value { color: #e5eaf3; }
:global(.dark) .stat-label { color: #a3a6ad; }
:global(.dark) .section-title { color: #e5eaf3; }
:global(.dark) .garden-name { color: #e5eaf3; }
:global(.dark) .garden-detail-row { color: #a3a6ad; }
:global(.dark) .stat-mini .value { color: #e5eaf3; }
:global(.dark) .garden-stats-row { border-top-color: #363637; }
</style>