<template>
  <div class="page-container">
    <div class="card header-card">
      <div class="page-title">计划任务</div>
      <el-button type="primary" icon="Plus" @click="handleAdd">新建任务</el-button>
    </div>

    <div class="card filter-card">
      <el-form :inline="true" :model="queryParams">
        <el-form-item label="任务名称">
          <el-input v-model="queryParams.name" placeholder="请输入任务名称" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="queryParams.type" placeholder="全部类型" clearable>
            <el-option label="Cron定时" value="cron" />
            <el-option label="一次性" value="once" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card table-card">
      <el-table :data="tableData" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" min-width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 'cron' ? 'primary' : 'warning'">{{ row.type === 'cron' ? '定时' : '一次性' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cron" label="Cron表达式" min-width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_run" label="上次执行" width="180">
          <template #default="{ row }">
            {{ formatTime(row.last_run) }}
          </template>
        </el-table-column>
         <el-table-column prop="enabled" label="启用" width="80">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleRun(row)">立即执行</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.size"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </div>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '新建任务'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="cron">Cron 定时</el-radio>
            <el-radio label="once">一次性执行</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Cron表达式" prop="cron" v-if="form.type === 'cron'">
          <el-input v-model="form.cron" placeholder="例如: 0 0 * * * (每天0点)">
             <template #append>
                <el-tooltip content="分 时 日 月 周" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
             </template>
          </el-input>
        </el-form-item>
        
        <el-divider content-position="left">执行动作</el-divider>
        
        <el-form-item label="目标类型" prop="target_type">
          <el-select v-model="form.target_type" placeholder="请选择">
            <el-option label="设备" value="device" />
            <el-option label="茶园" value="garden" />
            <el-option label="系统" value="system" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="动作类型" prop="action_type">
           <el-select v-model="form.action_type" placeholder="请选择">
            <el-option label="控制设备" value="control" />
            <el-option label="发送通知" value="notify" />
            <el-option label="生成报表" value="report" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="参数数据" prop="action_data">
           <el-input v-model="form.action_data" type="textarea" :rows="3" placeholder="JSON格式参数, 如: {'switch': 'on'}" />
        </el-form-item>
        
        <el-form-item label="是否启用">
           <el-switch v-model="form.enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getTaskList, createTask, updateTask, deleteTask, runTask } from '@/api/task'
import { Plus, Search, Refresh, QuestionFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const queryParams = reactive({
  page: 1,
  size: 10,
  name: '',
  type: ''
})

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentId = ref(null)

const form = reactive({
  name: '',
  type: 'cron',
  cron: '',
  target_type: 'device',
  target_id: null,
  action_type: 'control',
  action_data: '{}',
  enabled: true
})

const rules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  cron: [{ validator: (rule, value, callback) => {
      if (form.type === 'cron' && !value) {
          callback(new Error('请输入Cron表达式'))
      } else {
          callback()
      }
  }, trigger: 'blur' }]
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getTaskList(queryParams)
    tableData.value = res.list
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  fetchData()
}

const handleReset = () => {
  queryParams.name = ''
  queryParams.type = ''
  queryParams.page = 1
  fetchData()
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
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该任务吗?', '警告', {
    type: 'warning'
  }).then(async () => {
    try {
      await deleteTask(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (e) {}
  })
}

const handleRun = async (row) => {
    try {
        await runTask(row.id)
        ElMessage.success('指令已发送')
        fetchData()
    } catch(e) {}
}

const handleStatusChange = async (row) => {
    try {
        await updateTask(row.id, { enabled: row.enabled })
        ElMessage.success('状态更新成功')
    } catch(e) {
        row.enabled = !row.enabled // Revert
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return
    await formRef.value.validate(async (valid) => {
        if (valid) {
            submitting.value = true
            try {
                if (isEdit.value) {
                    await updateTask(currentId.value, form)
                    ElMessage.success('更新成功')
                } else {
                    await createTask(form)
                    ElMessage.success('创建成功')
                }
                dialogVisible.value = false
                fetchData()
            } catch (e) {
            } finally {
                submitting.value = false
            }
        }
    })
}

const resetForm = () => {
    form.name = ''
    form.type = 'cron'
    form.cron = ''
    form.target_type = 'device'
    form.action_type = 'control'
    form.action_data = '{}'
    form.enabled = true
}

const getStatusType = (status) => {
    if (status === 'success') return 'success'
    if (status === 'failed') return 'danger'
    if (status === 'running') return 'primary'
    return 'info'
}

const formatTime = (time) => {
    if (!time) return '-'
    return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}
.card {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 20px;
}
.header-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.page-title {
  font-size: 20px;
  font-weight: bold;
}
.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}
</style>
