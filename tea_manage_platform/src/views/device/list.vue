<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="eyebrow">设备管理</div>
        <div class="title">物联设备总览</div>
        <div class="sub">分组、状态、遥测一站式管理</div>
      </div>
      <el-button type="primary" icon="Plus">注册新设备</el-button>
    </div>

    <el-row :gutter="16">
      <el-col :span="5">
        <div class="card">
          <div class="card-title">产品分组</div>
          <el-tree :data="productTree" default-expand-all highlight-current />
        </div>
      </el-col>

      <el-col :span="19">
        <div class="card">
          <div class="toolbar">
            <el-input v-model="searchKey" placeholder="设备名称/ID" style="width: 220px" clearable />
            <el-space>
              <el-select v-model="status" placeholder="状态" style="width: 120px" clearable>
                <el-option label="全部" value="all" />
                <el-option label="在线" value="online" />
                <el-option label="离线" value="offline" />
              </el-select>
              <el-button type="primary" icon="Search">查询</el-button>
            </el-space>
          </div>

          <el-table :data="deviceList" style="width: 100%">
            <el-table-column prop="deviceName" label="设备名称" />
            <el-table-column prop="deviceSn" label="序列号" width="180" />
            <el-table-column prop="productName" label="所属产品" width="140" />
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <div class="flex-center">
                  <span class="dot" :class="row.isOnline ? 'bg-green' : 'bg-gray'"></span>
                  {{ row.isOnline ? '在线' : '离线' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="lastTime" label="最后上报时间" width="180" />
            <el-table-column label="最新遥测" show-overflow-tooltip>
              <template #default="{ row }">
                {{ JSON.stringify(row.telemetry) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220">
              <el-button link type="primary">查看曲线</el-button>
              <el-button link type="primary">调试</el-button>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchKey = ref('')
const status = ref('all')

const productTree = [
  {
    label: '全部产品',
    children: [
      { label: '土壤传感器 v1' },
      { label: '茶园气象站 v2' },
      { label: '水肥一体机' },
    ],
  },
]

const deviceList = ref([
  {
    deviceName: '1号地传感器',
    deviceSn: 'SN100293',
    productName: '土壤传感器 v1',
    isOnline: true,
    lastTime: '2023-10-27 10:00:00',
    telemetry: { humi: 20.5, temp: 15 },
  },
  {
    deviceName: '2号地传感器',
    deviceSn: 'SN100294',
    productName: '土壤传感器 v1',
    isOnline: false,
    lastTime: '2023-10-26 18:00:00',
    telemetry: {},
  },
])
</script>

<style scoped>
.page { padding: 20px; background: linear-gradient(180deg, #f7f9fb 0%, #f2f6f9 100%); min-height: 100%; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.eyebrow { font-size: 13px; color: #8c9ba8; letter-spacing: 1px; text-transform: uppercase; }
.title { font-size: 26px; font-weight: 700; color: #1f2a44; }
.sub { color: #6b7785; margin-top: 4px; }
.card { background: #fff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); padding: 16px; margin-bottom: 16px; }
.card-title { font-weight: 600; margin-bottom: 12px; color: #2d3a4a; }
.toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.flex-center { display: flex; align-items: center; gap: 6px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.bg-green { background: #16c06e; }
.bg-gray { background: #909399; }
</style>
