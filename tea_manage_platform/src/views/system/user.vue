<template>
  <div class="user-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">
        <el-icon class="mr-1"><Plus /></el-icon>新建用户
      </el-button>
    </div>

    <el-table :data="tableData" v-loading="loading" style="width: 100%" class="mt-4">
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="name" label="姓名" width="150" />
      <el-table-column label="角色" width="150">
        <template #default="scope">
          <el-tag v-for="role in scope.row.roles" :key="role" class="mr-1">{{ role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="权限" min-width="200">
        <template #default="scope">
          <el-tag v-for="perm in scope.row.permissions" :key="perm" type="info" class="mr-1 mb-1">{{ perm }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.size"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="fetchData"
      />
    </div>

    <!-- 用户表单弹窗 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="!!form.id" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!form.id">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-else>
          <el-input v-model="form.password" type="password" placeholder="留空则不修改" show-password />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="roles">
          <el-select v-model="form.roles" multiple placeholder="请选择角色">
            <el-option label="超级管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        
        <el-divider content-position="left">权限分配</el-divider>
        
        <el-form-item label="管理茶园">
          <el-select v-model="form.garden_ids" multiple placeholder="请选择管理的茶园">
            <el-option
              v-for="item in gardenList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="功能权限">
          <el-checkbox-group v-model="form.permissions">
            <div class="perm-group">
              <div class="group-title">茶园管理</div>
              <el-checkbox label="garden:create">新建茶园</el-checkbox>
              <el-checkbox label="garden:update">编辑茶园</el-checkbox>
              <el-checkbox label="garden:delete">删除茶园</el-checkbox>
            </div>
            <div class="perm-group">
              <div class="group-title">设备管理</div>
              <el-checkbox label="device:create">新建设备</el-checkbox>
              <el-checkbox label="device:update">编辑设备</el-checkbox>
              <el-checkbox label="device:delete">删除设备</el-checkbox>
            </div>
          </el-checkbox-group>
        </el-form-item>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser } from '@/api/user'
import { getTeaGardenList } from '@/api/tea-garden'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const queryParams = reactive({
  page: 1,
  size: 10,
  keyword: ''
})

const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const gardenList = ref([])

const form = reactive({
  id: undefined,
  username: '',
  password: '',
  name: '',
  roles: [],
  garden_ids: [],
  permissions: []
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }], // 仅新建时必填，逻辑在 submitForm 处理
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  roles: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const dialogTitle = computed(() => form.id ? '编辑用户' : '新建用户')

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getUserList(queryParams)
    tableData.value = res.list
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchGardens = async () => {
  try {
    const res = await getTeaGardenList({ page: 1, size: 100 }) // 获取所有茶园
    gardenList.value = res.list
  } catch (error) {
    console.error(error)
  }
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  resetForm()
  Object.assign(form, row)
  form.password = '' // 编辑时不回显密码
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除用户 "${row.username}" 吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error(error)
    }
  })
}

const submitForm = async () => {
  if (!formRef.value) return
  
  // 编辑时密码非必填
  if (form.id) {
    // 移除密码校验规则
    // 简单处理：如果密码为空，则不提交密码字段
  }

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (form.id) {
          const updateData = { ...form }
          if (!updateData.password) delete updateData.password
          await updateUser(form.id, updateData)
          ElMessage.success('更新成功')
        } else {
          await createUser(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  form.id = undefined
  form.username = ''
  form.password = ''
  form.name = ''
  form.roles = []
  form.garden_ids = []
  form.permissions = []
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(() => {
  fetchData()
  fetchGardens()
})
</script>

<style scoped>
.user-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.perm-group {
  margin-bottom: 10px;
}
.group-title {
  font-weight: bold;
  margin-bottom: 5px;
  color: #606266;
}
</style>
