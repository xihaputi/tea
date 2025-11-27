<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="eyebrow">设备管理</div>
        <div class="title">物联设备总览</div>
        <div class="sub">分组、状态、遥测一站式管理</div>
      </div>
      <el-button type="primary" icon="Plus" @click="handleAdd">注册新设备</el-button>
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
            <el-table-column prop="last_time" label="最后上报时间" width="180" />
            <el-table-column label="MQTT 账号" width="120" show-overflow-tooltip>
               <template #default="{ row }">
                 {{ row.mqtt_username || '-' }}
               </template>
            </el-table-column>
            <el-table-column label="操作" width="220">
              <template #default="{ row }">
                <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
                <el-button link type="primary">查看曲线</el-button>
                <el-button link type="primary">调试</el-button>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getProductGroups, getDeviceList, createDevice, updateDevice } from '@/api/device'
import { ElMessage } from 'element-plus'

const searchKey = ref('')
const status = ref('all')
const productTree = ref([])
const deviceList = ref([])
const loading = ref(false)

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

const rules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  sn: [{ required: true, message: '请输入设备序列号', trigger: 'blur' }],
  product_id: [{ required: true, message: '请选择所属产品', trigger: 'change' }]
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
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
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
</style>
