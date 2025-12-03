<template>
  <el-dialog
    v-model="visible"
    title="历史数据与曲线"
    width="900px"
    destroy-on-close
    @close="handleClose"
  >
    <div v-loading="loading" class="history-container">
      <!-- Toolbar -->
      <div class="toolbar">
        <el-space>
          <span class="label">时间范围:</span>
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            :shortcuts="shortcuts"
            @change="fetchData"
            style="width: 380px"
          />
          <el-button type="primary" icon="Refresh" @click="fetchData">刷新</el-button>
        </el-space>
      </div>

      <!-- Charts -->
      <div class="chart-container" ref="chartRef"></div>

      <!-- Data Table -->
      <div class="table-container">
        <div class="section-title">详细数据</div>
        <el-table :data="tableData" border style="width: 100%" height="300">
          <el-table-column prop="ts" label="时间" width="180">
            <template #default="{ row }">
              {{ formatTime(row.ts) }}
            </template>
          </el-table-column>
          <el-table-column 
            v-for="key in dataKeys" 
            :key="key" 
            :prop="key" 
            :label="getDisplayName(key)" 
          />
        </el-table>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getHistoryTelemetry } from '@/api/device'
import dayjs from 'dayjs'

const visible = ref(false)
const loading = ref(false)
const chartRef = ref(null)
let chartInstance = null
const currentDevice = ref(null)

// Helper to get display name for template
const getDisplayName = (key) => {
    if (!currentDevice.value) return key
    try {
        const config = JSON.parse(currentDevice.value.sensor_config || '{}')
        if (config[key] && config[key].name) {
            return config[key].name
        }
    } catch (e) {}
    return key
}

// Date Range (Default: Last 24 hours)
const dateRange = ref([
  dayjs().subtract(24, 'hour').toDate(),
  dayjs().toDate()
])

const shortcuts = [
  { text: '最近1小时', value: () => [dayjs().subtract(1, 'hour').toDate(), dayjs().toDate()] },
  { text: '最近24小时', value: () => [dayjs().subtract(24, 'hour').toDate(), dayjs().toDate()] },
  { text: '最近7天', value: () => [dayjs().subtract(7, 'day').toDate(), dayjs().toDate()] },
]

// Data
const tableData = ref([])
const dataKeys = ref([])

const open = (device) => {
  currentDevice.value = device
  visible.value = true
  // Reset date range if needed, or keep last selection
  nextTick(() => {
    initChart()
    fetchData()
  })
}

const handleClose = () => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
}

const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    window.addEventListener('resize', resizeChart)
  }
}

const resizeChart = () => {
  chartInstance?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  chartInstance?.dispose()
})

const fetchData = async () => {
  if (!currentDevice.value || !dateRange.value) return
  
  loading.value = true
  try {
    const [start, end] = dateRange.value
    const params = {
      startTs: dayjs(start).toISOString(),
      endTs: dayjs(end).toISOString()
    }
    
    // API returns: { "temp": [{ts, value}, ...], "humidity": [...] }
    const res = await getHistoryTelemetry(currentDevice.value.id, params)
    
    processData(res)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const processData = (data) => {
  if (!data || Object.keys(data).length === 0) {
    tableData.value = []
    dataKeys.value = []
    chartInstance?.clear()
    return
  }

  // 1. Extract Keys and Config
  const keys = Object.keys(data)
  dataKeys.value = keys
  
  // Parse config
  let config = {}
  try {
      config = JSON.parse(currentDevice.value.sensor_config || '{}')
  } catch (e) {}

  // Helper to get display name
  const getDisplayName = (key) => {
      if (config[key] && config[key].name) {
          return config[key].name
      }
      return key
  }
  
  // Helper to get unit
  const getUnit = (key) => {
      if (config[key] && config[key].unit) {
          return config[key].unit
      }
      return ''
  }

  // 2. Prepare Chart Series
  const series = keys.map(key => {
    return {
      name: getDisplayName(key), // Use display name
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: data[key].map(item => [new Date(item.ts), parseFloat(item.value)]),
      // Store unit in series for tooltip
      unit: getUnit(key) 
    }
  })

  // 3. Update Chart
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        let res = dayjs(params[0].value[0]).format('YYYY-MM-DD HH:mm:ss') + '<br/>'
        params.forEach(item => {
          // Find series to get unit (echarts params doesn't directly give custom props easily, 
          // but we can find by seriesName or index. 
          // Actually, we can just look up our config using the series name if unique, 
          // OR better: just use the series name which is already the display name.
          // But we want the unit. 
          // Let's try to find the series definition.
          const ser = series[item.seriesIndex]
          const unit = ser ? ser.unit : ''
          res += item.marker + item.seriesName + ': ' + item.value[1] + ' ' + unit + '<br/>'
        })
        return res
      }
    },
    legend: {
      data: series.map(s => s.name), // Use display names
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'time',
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series: series
  }
  
  chartInstance?.setOption(option, true)

  // 4. Prepare Table Data
  const timeMap = new Map()
  
  keys.forEach(key => {
    data[key].forEach(item => {
      const timeStr = item.ts
      if (!timeMap.has(timeStr)) {
        timeMap.set(timeStr, { ts: timeStr })
      }
      // Use display name as key for table? No, table columns are defined by dataKeys.
      // We should probably map dataKeys to display names in the template.
      timeMap.get(timeStr)[key] = item.value
    })
  })
  
  tableData.value = Array.from(timeMap.values()).sort((a, b) => new Date(b.ts) - new Date(a.ts))
}

const formatTime = (ts) => {
  return dayjs(ts).format('YYYY-MM-DD HH:mm:ss')
}

defineExpose({ open })
</script>

<style scoped>
.history-container {
  padding: 0 10px;
}
.toolbar {
  margin-bottom: 20px;
}
.label {
  font-weight: 500;
  color: #606266;
}
.chart-container {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #303133;
  border-left: 4px solid #409EFF;
  padding-left: 10px;
}
</style>
