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
             <el-tag effect="plain">{{ row.condition }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column label="执行动作 (Then)" min-width="250">
           <template #default="{row}">
             <el-tag type="warning" v-for="act in row.actions" :key="act" class="mr-1">{{ act }}</el-tag>
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
      <el-form label-width="100px">
        <el-form-item label="规则名称"><el-input placeholder="例如：土壤缺水告警" /></el-form-item>
        <el-form-item label="关联设备">
          <el-select placeholder="选择产品类型"><el-option label="土壤传感器" value="1"/></el-select>
        </el-form-item>
        
        <el-divider content-position="left">触发条件</el-divider>
        <el-form-item label="当">
          <el-row :gutter="10">
            <el-col :span="8"><el-select placeholder="字段" model-value="soil_moisture"/></el-col>
            <el-col :span="6"><el-select placeholder="操作符" model-value="<" /></el-col>
            <el-col :span="8"><el-input placeholder="阈值" model-value="20" /></el-col>
          </el-row>
          <div class="text-gray-400 text-xs mt-1">持续时长 > 10 分钟</div>
        </el-form-item>

        <el-divider content-position="left">执行动作</el-divider>
        <el-form-item label="动作">
          <el-checkbox-group v-model="actionList">
            <el-checkbox label="生成系统告警" />
            <el-checkbox label="发送小程序通知" />
            <el-checkbox label="发送短信" />
            <el-checkbox label="设备控制(开水泵)" />
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRuleList, enableRule } from '@/api/rule'
import { ElMessage } from 'element-plus'

const dialogVisible = ref(false)
const actionList = ref([])
const rules = ref([])
const loading = ref(false)

const fetchRules = async () => {
  loading.value = true
  try {
    const res = await getRuleList()
    if (res) {
      rules.value = res.list || []
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
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
})
</script>