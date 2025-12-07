<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="flex justify-between">
          <span>告警记录</span>
          <el-button icon="Refresh" @click="fetchData">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="tableData" v-loading="loading">
        <el-table-column prop="severity" label="级别" width="100">
            <template #default="{row}">
                <el-tag type="danger" v-if="row.severity==='critical'">严重</el-tag>
                <el-tag type="warning" v-else-if="row.severity==='warning'">警告</el-tag>
                <el-tag type="info" v-else>信息</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="content" label="告警内容" min-width="300" />
        <el-table-column prop="deviceName" label="关联设备" width="180" />
        <el-table-column prop="created_at" label="发生时间" width="180">
            <template #default="{row}">
                {{ new Date(row.created_at).toLocaleString() }}
            </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
            <template #default="{row}">
                <el-tag v-if="row.status==='active'" type="danger">激活</el-tag>
                <el-tag v-else-if="row.status==='acknowledged'" type="warning">已确认</el-tag>
                <el-tag v-else type="success">已清除</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="handlerName" label="处理人" width="120">
            <template #default="{row}">
                {{ row.handlerName || '-' }}
            </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
            <template #default="{row}">
                <el-button 
                    v-if="row.status==='active'" 
                    link type="primary" 
                    @click="handleAck(row)"
                >确认</el-button>
                <el-button 
                    v-if="row.status!=='cleared'" 
                    link type="success" 
                    @click="handleClear(row)"
                >清除</el-button>
            </template>
        </el-table-column>
      </el-table>
      
      <div class="mt-4 flex justify-end">
        <el-pagination 
          background 
          layout="prev, pager, next" 
          :total="total" 
          v-model:current-page="queryParams.page"
          @current-change="fetchData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getAlarmList, acknowledgeAlarm, clearAlarm } from '@/api/alarm'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const queryParams = reactive({
    page: 1,
    size: 10
})

const fetchData = async () => {
    loading.value = true
    try {
        const res = await getAlarmList(queryParams)
        tableData.value = res.list || []
        total.value = res.total || 0
    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

const handleAck = async (row) => {
    try {
        await acknowledgeAlarm(row.id)
        ElMessage.success('已确认')
        fetchData()
    } catch (error) {
        console.error(error)
    }
}

const handleClear = async (row) => {
    try {
        await clearAlarm(row.id)
        ElMessage.success('已清除')
        fetchData()
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchData()
})
</script>
