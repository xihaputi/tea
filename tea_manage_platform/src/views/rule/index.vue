<!-- src/views/rule/index.vue -->
<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" type="card" class="demo-tabs">
        <el-tab-pane label="状态映射规则" name="status">
            <el-card shadow="never">
                <template #header>
                    <div class="flex justify-between items-center">
                        <div class="flex items-center gap-4">
                            <div>
                                <span class="font-bold text-lg">传感器状态映射</span>
                                <div class="text-gray-400 text-xs mt-1">根据设备类型配置传感器状态显示规则</div>
                            </div>
                            <el-select v-model="selectedProduct" placeholder="请选择设备类型以配置" @change="handleProductSelect" style="width: 200px">
                                <el-option v-for="p in products" :key="p.id" :label="p.label" :value="p.id" />
                            </el-select>
                        </div>
                        <div v-if="!selectedProduct">
                            <el-alert type="info" show-icon :closable="false">请先选择设备类型</el-alert>
                        </div>
                    </div>
                </template>
                
                <!-- 当选择了产品时，显示该产品的传感器列表 -->
                <div v-if="selectedProduct">
                     <el-table :data="productSensors" v-loading="statusLoading" empty-text="未找到该产品的传感器配置或无设备">
                        <el-table-column prop="name" label="传感器名称" width="180">
                             <template #default="{row}">
                                <span class="font-bold">{{ row.name }}</span>
                             </template>
                        </el-table-column>
                        <el-table-column prop="key" label="标识 (Key)" width="150">
                             <template #default="{row}">
                                <el-tag type="info" size="small">{{ row.key }}</el-tag>
                             </template>
                        </el-table-column>
                        <el-table-column label="当前状态规则" min-width="400">
                            <template #default="{row}">
                                <div v-if="row.rule" class="flex flex-wrap gap-2">
                                    <el-tag 
                                        v-for="(cfg, idx) in parseRuleConfig(row.rule.rule_config)" 
                                        :key="idx"
                                        :color="cfg.color" 
                                        effect="dark"
                                        style="border: none;"
                                    >
                                        {{ formatRange(cfg) }} : {{ cfg.label }}
                                    </el-tag>
                                </div>
                                <span v-else class="text-gray-400 text-sm">暂无配置，显示默认数值</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="120" fixed="right">
                            <template #default="{row}">
                                <el-button type="primary" link @click="openConfigDialog(row)">
                                    {{ row.rule ? '修改配置' : '去配置' }}
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <!-- 未选择产品时，显示所有已配置规则 (可选，或者直接留空) -->
                <div v-else class="text-center py-10 text-gray-400">
                    <el-icon :size="48"><Operation /></el-icon>
                    <div class="mt-2">请在左上角选择设备类型，以查看和配置对应的传感器规则</div>
                </div>
            </el-card>
        </el-tab-pane>
        
        <el-tab-pane label="告警触发规则" name="alarm">
             <el-card shadow="never">
              <template #header>
                <div class="flex justify-between">
                  <span>自动化告警规则列表</span>
                  <el-button type="primary" icon="Plus" @click="dialogVisible = true">新建告警规则</el-button>
                </div>
              </template>
              
              <el-table :data="rules">
                <el-table-column prop="name" label="规则名称" width="200" />
                <el-table-column label="触发条件 (If)" min-width="250">
                   <template #default="{row}">
                     <el-tag effect="plain" v-if="row.input_key">
                        {{ row.input_key }} {{ row.operator }} {{ row.threshold }}
                     </el-tag>
                     <span v-else>{{ row.condition }}</span>
                   </template>
                </el-table-column>
                <el-table-column label="执行动作 (Then)" min-width="250">
                   <template #default="{row}">
                     <el-tag type="warning">生成系统告警</el-tag>
                   </template>
                </el-table-column>
                <el-table-column prop="enabled" label="启用" width="100">
                  <template #default="{row}">
                    <el-switch v-model="row.enabled" @change="handleSwitchChange(row)" />
                  </template>
                </el-table-column>
                 <el-table-column label="操作" width="100">
                    <template #default="{row}">
                         <el-button link type="danger" @click="handleDeleteRule(row)">删除</el-button>
                    </template>
                 </el-table-column>
              </el-table>
            </el-card>
        </el-tab-pane>
    </el-tabs>

    <!-- 状态规则配置弹窗 -->
    <el-dialog v-model="statusDialogVisible" title="配置状态规则" width="700px">
        <el-form :model="statusForm" label-width="100px">
            <div class="bg-gray-50 p-4 rounded mb-4">
                 <div class="font-bold mb-2">{{ currentSensorName }} ({{ statusForm.sensor_key }})</div>
                 <div class="text-xs text-gray-500">为该传感器配置不同数值区间对应的状态显示</div>
            </div>

            <el-form-item label="规则模板">
                <el-select placeholder="选择模板快速填充" @change="applyTemplate">
                    <el-option label="空气温度标准" value="air_temp" />
                    <el-option label="空气湿度标准" value="humidity" />
                    <el-option label="土壤水分标准" value="soil_humi" />
                    <el-option label="土壤PH标准" value="soil_ph" />
                     <el-option label="光照强度标准" value="lux" />
                </el-select>
            </el-form-item>
            
            <el-form-item label="规则名称">
                <el-input v-model="statusForm.name" placeholder="例如：空气温度判断标准" />
            </el-form-item>
            
            <el-form-item label="状态定义">
                <div class="w-full">
                    <div v-for="(item, index) in statusForm.config" :key="index" class="flex gap-2 mb-2 items-center">
                        <el-input-number v-model="item.min" :controls="false" placeholder="Min" style="width: 80px" />
                        <span>≤ 值 &lt;</span>
                        <el-input-number v-model="item.max" :controls="false" placeholder="Max" style="width: 80px" />
                        <el-input v-model="item.label" placeholder="状态名称" style="width: 120px" />
                        <el-color-picker v-model="item.color" show-alpha />
                        <el-button circle icon="Delete" type="danger" link @click="removeStatusItem(index)" />
                    </div>
                    <el-button type="primary" link icon="Plus" @click="addStatusItem">添加状态区间</el-button>
                </div>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="statusDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitStatusRule">保存配置</el-button>
        </template>
    </el-dialog>

    <!-- 告警规则弹窗 (Existing) -->
    <el-dialog v-model="dialogVisible" title="配置告警规则" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="规则名称"><el-input v-model="form.name" placeholder="例如：土壤缺水告警" /></el-form-item>
        <el-form-item label="关联产品">
          <el-select v-model="form.product_id" placeholder="选择产品类型" @change="handleProductChange">
             <el-option v-for="p in products" :key="p.id" :label="p.label" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联设备">
          <el-select v-model="form.device_id" placeholder="可选：指定特定设备" clearable>
             <el-option v-for="d in devices" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
          <div class="text-gray-400 text-xs">不选则应用于该产品下的所有设备</div>
        </el-form-item>
        
        <el-divider content-position="left">触发条件</el-divider>
        <el-form-item label="当">
          <el-row :gutter="10">
            <el-col :span="8"><el-input v-model="form.input_key" placeholder="字段 (如 temperature)"/></el-col>
            <el-col :span="6">
                <el-select v-model="form.operator" placeholder="操作符">
                    <el-option label=">" value=">" />
                    <el-option label="<" value="<" />
                    <el-option label="=" value="=" />
                    <el-option label=">=" value=">=" />
                    <el-option label="<=" value="<=" />
                </el-select>
            </el-col>
            <el-col :span="8"><el-input v-model.number="form.threshold" placeholder="阈值" /></el-col>
          </el-row>
        </el-form-item>
      </el-form>
      <template #footer>
           <el-button @click="dialogVisible = false">取消</el-button>
           <el-button type="primary" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getRuleList, createRule, enableRule, deleteRule, getSensorRules, createSensorRule, updateSensorRule, deleteSensorRule } from '@/api/rule'
import { getProductGroups, getDeviceList } from '@/api/device'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('status')
const statusLoading = ref(false)

// Status Rules State
const selectedProduct = ref(null)
const productSensors = ref([]) // List of {name, key, rule}
const statusRulesMap = ref({}) // key -> rule object

const statusDialogVisible = ref(false)
const currentStatusRuleId = ref(null)
const currentSensorName = ref('')
const statusForm = reactive({
    name: '',
    sensor_key: '',
    config: []
})

// Alarm Rules State
const dialogVisible = ref(false)
const actionList = ref(['生成系统告警'])
const rules = ref([])
const products = ref([])
const devices = ref([])
const form = reactive({
    name: '',
    product_id: null,
    device_id: null,
    input_key: '',
    operator: '>',
    threshold: null
})

// --- Status Rules Logic ---

const fetchStatusRules = async () => {
    try {
        const res = await getSensorRules()
        const map = {}
        if (res) {
            res.forEach(r => { map[r.sensor_key] = r })
        }
        statusRulesMap.value = map
    } catch (e) {
        console.error(e)
    }
}

const handleProductSelect = async (pid) => {
    statusLoading.value = true
    productSensors.value = []
    try {
        // 1. Ensure rules are loaded
        await fetchStatusRules()
        
        // 2. Fetch sample device to get config
        // Note: Backend param is productId (camelCase)
        const res = await getDeviceList({ productId: pid, size: 1 })
        
        if (res && res.list && res.list.length > 0) {
            const device = res.list[0]
            if (device.sensor_config) {
                try {
                    const config = JSON.parse(device.sensor_config)
                    const list = []
                    for (const key in config) {
                        if (key === '__ignored') continue
                        const item = config[key]
                        list.push({
                            key: key,
                            name: item.name || key,
                            rule: statusRulesMap.value[key] || null
                        })
                    }
                    productSensors.value = list
                } catch (e) {
                    console.error('Parse config error', e)
                    ElMessage.warning('设备配置解析失败')
                }
            } else {
                 ElMessage.info('该类型设备暂无默认传感器配置')
            }
        } else {
            ElMessage.warning('未找到该类型的设备，无法加载传感器列表')
        }
        
    } catch (e) {
        console.error(e)
        ElMessage.error('加载传感器失败')
    } finally {
        statusLoading.value = false
    }
}

const openConfigDialog = (row) => {
    currentSensorName.value = row.name
    statusForm.sensor_key = row.key
    statusForm.name = row.rule ? row.rule.name : (row.name + '状态规则')
    currentStatusRuleId.value = row.rule ? row.rule.id : null
    
    if (row.rule) {
        statusForm.config = parseRuleConfig(row.rule.rule_config)
    } else {
        // Default template
        statusForm.config = [
            { min: 0, max: 100, label: '正常', color: '#67C23A' }
        ]
        // Auto apply template if name matches known types
        if (row.name.includes('温度')) applyTemplate('air_temp')
        else if (row.name.includes('湿度')) applyTemplate('humidity')
        else if (row.name.includes('土壤')) applyTemplate('soil_humi')
    }
    
    statusDialogVisible.value = true
}

const parseRuleConfig = (jsonStr) => {
    try {
        return JSON.parse(jsonStr)
    } catch (e) {
        return []
    }
}

const formatRange = (cfg) => {
    const min = cfg.min !== null && cfg.min !== undefined ? cfg.min : ''
    const max = cfg.max !== null && cfg.max !== undefined ? cfg.max : ''
    if (min === '' && max === '') return 'Any'
    if (min === '') return `< ${max}`
    if (max === '') return `≥ ${min}`
    return `${min} ~ ${max}`
}

const addStatusItem = () => {
    statusForm.config.push({ min: null, max: null, label: '', color: '#409EFF' })
}

const removeStatusItem = (index) => {
    statusForm.config.splice(index, 1)
}

const applyTemplate = (val) => {
    if (val === 'air_temp') {
        statusForm.config = [
            { min: 18, max: 30, label: '适宜生长', color: '#67C23A' },
            { min: 32, max: null, label: '高温风险', color: '#F56C6C' },
            { min: null, max: 5, label: '低温风险', color: '#409EFF' }
        ]
    } else if (val === 'humidity') {
        statusForm.config = [
            { min: 70, max: 90, label: '适宜', color: '#67C23A' },
            { min: null, max: 60, label: '干燥', color: '#E6A23C' },
            { min: 95, max: null, label: '高湿风险', color: '#F56C6C' }
        ]
    } else if (val === 'soil_humi') {
        statusForm.config = [
            { min: 60, max: 80, label: '适宜', color: '#67C23A' },
            { min: null, max: 50, label: '轻度干旱', color: '#E6A23C' },
            { min: 90, max: null, label: '渍害风险', color: '#F56C6C' }
        ]
    } else if (val === 'soil_ph') {
         statusForm.config = [
            { min: 4.5, max: 5.5, label: '最适区间', color: '#67C23A' },
            { min: null, max: 4.2, label: '酸化风险', color: '#E6A23C' },
            { min: 5.8, max: null, label: '偏碱风险', color: '#F56C6C' }
        ]
    } else if (val === 'lux') {
         statusForm.config = [
            { min: 10000, max: 50000, label: '光照适宜', color: '#67C23A' },
            { min: null, max: 5000, label: '光照不足', color: '#E6A23C' },
            { min: 80000, max: null, label: '强光灼伤', color: '#F56C6C' }
        ]
    }
}

const submitStatusRule = async () => {
    try {
        const payload = {
            name: statusForm.name,
            sensor_key: statusForm.sensor_key,
            rule_config: JSON.stringify(statusForm.config)
        }
        if (currentStatusRuleId.value) {
            await updateSensorRule(currentStatusRuleId.value, payload)
        } else {
            await createSensorRule(payload)
        }
        ElMessage.success('配置已保存')
        statusDialogVisible.value = false
        // Refresh
        await fetchStatusRules()
        if (selectedProduct.value) {
            // Re-render table row
            await handleProductSelect(selectedProduct.value)
        }
    } catch (e) {
        console.error(e)
    }
}

// --- Alarm Rules Logic ---

const fetchRules = async () => {
  try {
    const res = await getRuleList()
    if (res) {
      rules.value = res.list || []
    }
  } catch (error) {
    console.error(error)
  }
}

const handleDeleteRule = async (row) => {
    ElMessageBox.confirm('确认删除?', '提示').then(async () => {
        await deleteRule(row.id)
        fetchRules()
    })
}

const fetchProducts = async () => {
    const res = await getProductGroups()
    products.value = res || []
}

const handleProductChange = async (val) => {
    form.device_id = null
    const res = await getDeviceList({ productId: val, size: 100 })
    devices.value = res.list || []
}

const handleSubmit = async () => {
    try {
         await createRule(form)
         ElMessage.success('规则创建成功')
         dialogVisible.value = false
         fetchRules()
    } catch (error) {
        console.error(error)
    }
}

const handleSwitchChange = async (row) => {
  try {
    await enableRule(row.id, row.enabled)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.enabled = !row.enabled 
    console.error(error)
  }
}

onMounted(() => {
  fetchStatusRules()
  fetchRules()
  fetchProducts()
})
</script>