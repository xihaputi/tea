<!-- src/views/tea-garden/detail.vue -->
<template>
  <div class="app-container">
    <div class="header mb-20">
      <el-page-header @back="$router.back()" title="返回列表">
        <template #content>
          <span class="text-large font-600 mr-3">西湖龙井一号基地</span>
          <el-tag type="success">运营中</el-tag>
        </template>
      </el-page-header>
    </div>

    <el-tabs v-model="activeTab" type="border-card">
      
      <!-- Tab 1: 基础信息 -->
      <el-tab-pane label="基础信息" name="info">
        <el-form label-width="100px" style="max-width: 600px;">
          <el-form-item label="茶园名称"><el-input v-model="form.name" /></el-form-item>
          <el-form-item label="地理位置"><el-input v-model="form.address" /><el-button link>地图选点</el-button></el-form-item>
          <el-form-item label="种植面积"><el-input v-model="form.area"><template #append>亩</template></el-input></el-form-item>
          <el-form-item label="茶园简介"><el-input type="textarea" v-model="form.desc" /></el-form-item>
          <el-form-item> <el-button type="primary">保存更改</el-button> </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- Tab 2: 地块管理 -->
      <el-tab-pane label="地块管理" name="plots">
        <div class="mb-10"><el-button type="primary" icon="Plus">新增地块</el-button></div>
        <el-table :data="plotsData" border>
          <el-table-column prop="code" label="地块编号" width="120" />
          <el-table-column prop="variety" label="品种" width="120" />
          <el-table-column prop="area" label="面积(亩)" width="100" />
          <el-table-column label="关联设备">
             <template #default="scope">
               <el-tag v-for="dev in scope.row.devices" :key="dev" size="small" class="mr-1">{{ dev }}</el-tag>
             </template>
          </el-table-column>
          <el-table-column label="阈值模板" width="150">
             <template #default>
               <el-select placeholder="选择模板" size="small"><el-option label="成茶缺水预警" value="1"/></el-select>
             </template>
          </el-table-column>
          <el-table-column label="操作" width="150"><el-button link type="primary">编辑</el-button></el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- Tab 3: 已绑定设备 -->
      <el-tab-pane label="物联设备" name="devices">
        <el-table :data="deviceData">
          <el-table-column prop="name" label="设备名称" />
          <el-table-column prop="type" label="类型" />
          <el-table-column prop="status" label="状态">
             <template #default="{row}">
               <el-tag :type="row.status === 'online' ? 'success' : 'info'">{{ row.status }}</el-tag>
             </template>
          </el-table-column>
          <el-table-column label="实时数据(Preview)">
             <template #default>土壤湿度: 18% | 温度: 24℃</template>
          </el-table-column>
          <el-table-column label="操作">
             <el-button link type="danger">解绑</el-button>
          </el-table-column>
        </el-table>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('plots')

// 模拟表单数据
const form = reactive({
  name: '西湖龙井一号基地',
  address: '杭州市西湖区转塘街道',
  area: '50',
  desc: '核心产区，重点数字化监控区域。'
})

// 模拟地块数据
const plotsData = ref([
  { code: 'A-01', variety: '龙井43', area: 10, devices: ['土壤传感器#1', '气象站'] },
  { code: 'A-02', variety: '群体种', area: 15, devices: ['土壤传感器#2'] },
])

// 模拟设备数据
const deviceData = ref([
  { name: '土壤传感器#1', type: '传感器', status: 'online' },
  { name: '茶园气象站', type: '网关', status: 'online' },
  { name: '监控摄像头A', type: '摄像头', status: 'offline' },
])
</script>