<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="eyebrow">设备管理</div>
        <div class="title">物联设备总览</div>
        <div class="sub">分组、状态、遥测一站式管理</div>
      </div>
      <el-button type="primary" icon="Plus" @click="handleAdd" v-permission="['admin', 'super_admin']">注册新设备</el-button>
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
              <el-button type="primary" icon="Search" @click="handleSearch">查询</el-button>
            </el-space>
          </div>

          <el-table :data="deviceList" style="width: 100%">
            <el-table-column prop="name" label="设备名称" />
            <el-table-column prop="sn" label="序列号" width="180" />
            <el-table-column prop="productName" label="所属产品" width="140" />
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <div class="flex-center">
                  <span class="dot" :class="row.status === 'online' ? 'bg-green' : 'bg-gray'"></span>
                  {{ row.status === 'online' ? '在线' : '离线' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="实时数据" min-width="200">
              <template #default="{ row }">
                <div v-if="row.sensor_config">
                  <el-tag 
                    v-for="(cfg, key) in parseSensorConfig(row.sensor_config)" 
                    :key="key" 
                    v-show="cfg.show"
                    size="small" 
                    style="margin-right: 4px; margin-bottom: 4px;"
                  >
                    {{ cfg.name || key }}: {{ getSensorValue(row, key) }} {{ cfg.unit || '' }}
                  </el-tag>
                </div>
                <span v-else class="text-gray-400 text-xs">未配置</span>
              </template>
            </el-table-column>
            <el-table-column prop="last_time" label="最后上报时间" width="180" />
            <el-table-column label="MQTT 账号" width="120" show-overflow-tooltip>
               <template #default="{ row }">
                 {{ row.mqtt_username || '-' }}
               </template>
            </el-table-column>
            <el-table-column label="操作" width="220">
              <template #default="{ row }">
                <el-button link type="primary" @click="handleEdit(row)" v-permission="['admin', 'super_admin']">编辑</el-button>
                <el-button link type="primary" @click="handleCurve(row)">查看曲线</el-button>
                <el-button link type="primary" @click="handleDebug(row)" v-permission="['admin', 'super_admin']">调试</el-button>
                <el-button link type="danger" @click="handleDelete(row)" v-permission="['admin', 'super_admin']">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '注册新设备'" width="500px">
      <el-form :model="form" label-width="100px" ref="formRef" :rules="rules">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备序列号" prop="sn">
          <el-input v-model="form.sn" placeholder="唯一标识，如 MAC 地址" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="所属产品" prop="product_id">
          <el-select v-model="form.product_id" placeholder="请选择" style="width: 100%">
            <el-option v-for="item in productTree" :key="item.id" :label="item.label" :value="item.id" />
          </el-select>
        </el-form-item>
        
        <el-divider content-position="left">MQTT 配置指南</el-divider>
        <el-form-item label="上报话题">
            <el-input :value="computedTopic" readonly>
                <template #append>
                    <el-button @click="copyTopic(computedTopic)" icon="CopyDocument" />
                </template>
            </el-input>
            <div class="text-gray-400 text-xs mt-1">格式: tea/{类型}/{序列号}/telemetry</div>
        </el-form-item>

        <el-form-item label="订阅话题" v-if="computedSubTopic">
            <el-input :value="computedSubTopic" readonly>
                <template #append>
                    <el-button @click="copyTopic(computedSubTopic)" icon="CopyDocument" />
                </template>
            </el-input>
             <div class="text-gray-400 text-xs mt-1">设备需订阅此话题以接收控制指令</div>
        </el-form-item>


        <el-divider content-position="left">MQTT 认证信息</el-divider>
        <el-form-item label="MQTT 用户名" prop="mqtt_username">
          <el-input v-model="form.mqtt_username" placeholder="设备连接 MQTT 的用户名" />
        </el-form-item>
        <el-form-item label="MQTT 密码" prop="mqtt_password">
          <el-input v-model="form.mqtt_password" placeholder="设备连接 MQTT 的密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 调试/配置弹窗 -->
    <el-dialog v-model="debugVisible" title="传感器配置" width="710px">
      <div v-loading="debugLoading">
        <div class="mb-4 text-gray-500 text-sm flex-center" style="justify-content: space-between;">
          <span>检测到以下传感器数据键值 (基于最近10条遥测数据)：</span>
          <el-space>
            <el-button type="warning" link @click="handleStandardizeKeys">一键标准化</el-button>
            <el-button type="primary" link icon="Plus" @click="handleAddSensor">添加传感器</el-button>
          </el-space>
        </div>
        <el-table :data="debugSensors" border style="width: 100%">
          <el-table-column label="原始键名 (Key)" width="150">
            <template #default="{ row }">
              <el-input v-model="row.key" placeholder="例如: sensor1" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="显示名称" width="160">
            <template #default="{ row }">
              <el-input v-model="row.name" placeholder="例如: 温度" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="单位" width="100">
            <template #default="{ row }">
              <el-input v-model="row.unit" placeholder="℃" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="当前值" width="100">
             <template #default="{ row }">
               {{ row.value }}
             </template>
          </el-table-column>
          <el-table-column label="列表显示" align="center" width="90">
            <template #default="{ row }">
              <el-switch v-model="row.show" />
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" width="80">
            <template #default="{ row, $index }">
              <el-button type="danger" link icon="Delete" @click="handleDeleteSensor($index)" />
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="debugVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveConfig" :loading="savingConfig">保存配置</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 历史数据弹窗 -->
    <DeviceHistory ref="historyRef" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getProductGroups, getDeviceList, createDevice, updateDevice, getLatestTelemetry, deleteDevice } from '@/api/device'
import { ElMessage, ElMessageBox } from 'element-plus'
import DeviceHistory from './components/DeviceHistory.vue'

const searchKey = ref('')
const status = ref('all')
const productTree = ref([])
const deviceList = ref([])
const loading = ref(false)

// 历史数据相关
const historyRef = ref(null)

// 新增/编辑相关
const dialogVisible = ref(false)
const submitting = ref(false)
const isEdit = ref(false)
const currentId = ref(null)
const formRef = ref(null)
const form = reactive({
  name: '',
  sn: '',
  product_id: null,
  mqtt_username: '',
  mqtt_password: ''
})

// 调试/配置相关
const debugVisible = ref(false)
const debugLoading = ref(false)
const savingConfig = ref(false)
const currentDevice = ref(null)
const debugSensors = ref([])

const rules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  sn: [{ required: true, message: '请输入设备序列号', trigger: 'blur' }],
  product_id: [{ required: true, message: '请选择所属产品', trigger: 'change' }]
}



const fetchDevices = async () => {
  loading.value = true
  try {
    const params = {
      keyword: searchKey.value,
      status: status.value === 'all' ? undefined : status.value
    }
    const res = await getDeviceList(params)
    if (res) {
      deviceList.value = res.list || []
      // 预加载每个设备的最新遥测数据，用于列表显示
      deviceList.value.forEach(dev => {
         fetchDeviceTelemetry(dev)
      })
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchDeviceTelemetry = async (device) => {
    try {
        const res = await getLatestTelemetry(device.id)
        if (res) {
            device.telemetryData = {}
            res.forEach(item => {
                device.telemetryData[item.key] = item.value
            })
        }
    } catch (e) {
        console.error(e)
    }
}

const parseSensorConfig = (jsonStr) => {
    if (!jsonStr) return {}
    try {
        return JSON.parse(jsonStr)
    } catch (e) {
        return {}
    }
}

const getSensorValue = (row, key) => {
    if (row.telemetryData && row.telemetryData[key] !== undefined) {
        return row.telemetryData[key]
    }
    return '-'
}

const handleSearch = () => {
  fetchDevices()
}

const handleAdd = () => {
  isEdit.value = false
  currentId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  currentId.value = row.id
  form.name = row.name
  form.sn = row.sn
  form.product_id = row.product_id
  form.mqtt_username = row.mqtt_username || ''
  form.mqtt_password = row.mqtt_password || ''
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.prompt('此操作将永久删除该设备及其所有历史数据，不可恢复！请输入“确认删除设备”以确认。', '危险操作', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    inputPattern: /^确认删除设备$/,
    inputErrorMessage: '输入内容不正确',
    type: 'error'
  }).then(async ({ value }) => {
    try {
      await deleteDevice(row.id)
      ElMessage.success('设备已删除')
      fetchDevices()
    } catch (error) {
      console.error(error)
    }
  }).catch(() => {
    // 取消删除
  })
}

const handleDebug = async (row) => {
    currentDevice.value = row
    debugVisible.value = true
    debugLoading.value = true
    debugSensors.value = []
    
    try {
        // 1. 获取最新遥测数据
        const res = await getLatestTelemetry(row.id)
        // 2. 解析现有配置
        const config = parseSensorConfig(row.sensor_config)
        const ignoredKeys = new Set(config.__ignored || [])
        
        // 3. 合并数据
        const map = new Map()
        
        // 先加入已有配置的 Key (排除被忽略的)
        Object.keys(config).forEach(key => {
            if (key === '__ignored') return
            map.set(key, {
                key: key,
                name: config[key].name || key,
                unit: config[key].unit || '', // Add unit
                show: config[key].show || false,
                value: '-'
            })
        })
        
        // 再加入最新遥测的 Key
        if (res) {
            res.forEach(item => {
                // 如果在忽略列表中，且不在当前配置中（防止误删后又想加回来），则跳过
                if (ignoredKeys.has(item.key) && !map.has(item.key)) {
                    return
                }

                if (map.has(item.key)) {
                    map.get(item.key).value = item.value
                } else {
                    map.set(item.key, {
                        key: item.key,
                        name: item.key,
                        unit: '', // Default unit empty
                        show: false,
                        value: item.value
                    })
                }
            })
        }
        
        debugSensors.value = Array.from(map.values())
        
    } catch (error) {
        console.error(error)
        ElMessage.error('获取数据失败')
    } finally {
        debugLoading.value = false
    }
}

const handleAddSensor = () => {
    // 1. Find max sensor number
    let maxNum = 0
    debugSensors.value.forEach(item => {
        const match = item.key.match(/^sensor(\d+)$/)
        if (match) {
            const num = parseInt(match[1])
            if (num > maxNum) maxNum = num
        }
    })
    
    // 2. Generate new key
    const newKey = `sensor${maxNum + 1}`
    
    // 3. Add to list
    debugSensors.value.push({
        key: newKey,
        name: '',
        unit: '',
        show: true,
        value: '-' // No value yet
    })
}

const handleStandardizeKeys = () => {
    ElMessageBox.confirm(
        '此操作将把所有键名重命名为 sensor1, sensor2... 格式，且不可撤销。请确保设备端也同步修改发送的键名。是否继续？',
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        debugSensors.value.forEach((item, index) => {
            item.key = `sensor${index + 1}`
        })
        ElMessage.success('键名已标准化，请点击保存配置')
    }).catch(() => {})
}

const handleDeleteSensor = (index) => {
    debugSensors.value.splice(index, 1)
}

const handleSaveConfig = async () => {
    savingConfig.value = true
    try {
        const config = {}
        const currentKeys = new Set()
        
        debugSensors.value.forEach(item => {
            config[item.key] = {
                name: item.name,
                unit: item.unit, // Save unit
                show: item.show
            }
            currentKeys.add(item.key)
        })
        
        // 计算忽略列表：在最新遥测中存在，但在当前配置中不存在的 Key
        const ignored = []
        if (currentDevice.value.telemetryData) {
            Object.keys(currentDevice.value.telemetryData).forEach(key => {
                if (!currentKeys.has(key)) {
                    ignored.push(key)
                }
            })
        }
        // 保留之前的忽略列表（如果它们还没被加回来的话）
        const oldConfig = parseSensorConfig(currentDevice.value.sensor_config)
        if (oldConfig.__ignored) {
            oldConfig.__ignored.forEach(key => {
                if (!currentKeys.has(key) && !ignored.includes(key)) {
                    ignored.push(key)
                }
            })
        }
        
        if (ignored.length > 0) {
            config['__ignored'] = ignored
        }
        
        await updateDevice(currentDevice.value.id, {
            sensor_config: JSON.stringify(config)
        })
        
        ElMessage.success('配置已保存')
        debugVisible.value = false
        fetchDevices() // 刷新列表
    } catch (error) {
        console.error(error)
        ElMessage.error('保存失败')
    } finally {
        savingConfig.value = false
    }
}

const handleCurve = (row) => {
    historyRef.value.open(row)
}

const resetForm = () => {
  form.name = ''
  form.sn = ''
  form.product_id = null
  form.mqtt_username = ''
  form.mqtt_password = ''
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          await updateDevice(currentId.value, form)
          ElMessage.success('更新成功')
        } else {
          await createDevice(form)
          ElMessage.success('注册成功')
        }
        dialogVisible.value = false
        fetchDevices()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const fetchProducts = async () => {
  try {
    const res = await getProductGroups()
    if (res) {
      productTree.value = res
    }
  } catch (error) {
    console.error(error)
  }
}

const copyTopic = (text) => {
    navigator.clipboard.writeText(text).then(() => {
        ElMessage.success('已复制')
    }).catch(() => {
        ElMessage.error('复制失败')
    })
}

const computedTopic = computed(() => {
    const sn = form.sn || '{序列号}'
    let topicType = '{type}' 
    
    if (form.product_id) {
        const product = productTree.value.find(p => p.id === form.product_id)
        
        if (product) {
            const label = product.label
            if (label.includes('气象站')) topicType = 'weather'
            else if (label.includes('土壤')) topicType = 'sensor'
            else if (label.includes('阀门') || label.includes('水肥')) topicType = 'contral'
            else topicType = 'device'
        }
    }
    return `tea/${topicType}/${sn}/telemetry`
})


const computedSubTopic = computed(() => {
    const pub = computedTopic.value
    if (pub.includes('contral')) {
        return pub.replace('telemetry', 'sub')
    }
    return ''
})


onMounted(() => {
  fetchProducts()
  fetchDevices()
})
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
.mb-4 { margin-bottom: 16px; }
.text-gray-500 { color: #909399; }
.text-sm { font-size: 14px; }
.text-xs { font-size: 12px; }
.text-gray-400 { color: #c0c4cc; }
</style>
