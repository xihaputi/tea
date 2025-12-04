<!-- src/views/rule/index.vue -->
<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="flex justify-between">
          <span>自动化规则列表</span>
          <el-button type="primary" icon="Plus" @click="dialogVisible = true">新建规则</el-button>
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
      </el-table>
    </el-card>

    <!-- 新建规则弹窗 -->
    <el-dialog v-model="dialogVisible" title="配置规则" width="600px">
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

        <el-divider content-position="left">执行动作</el-divider>
        <el-form-item label="动作">
          <el-checkbox-group v-model="actionList">
            <el-checkbox label="生成系统告警" disabled checked />
            <el-checkbox label="发送短信" />
          </el-checkbox-group>
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
import { getRuleList, createRule, enableRule } from '@/api/rule'
import { getProductGroups, getDeviceList } from '@/api/device'
import { ElMessage } from 'element-plus'

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
    row.enabled = !row.enabled // 恢复状态
    console.error(error)
  }
}

onMounted(() => {
  fetchRules()
  fetchProducts()
})
</script>