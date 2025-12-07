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
          <el-button link type="warning" @click="handleImpersonate(scope.row)" v-permission="['super_admin']">身份登录</el-button>
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
        
        <el-form-item label="用户角色" prop="roles">
          <el-select v-model="form.roles" placeholder="请选择角色" @change="handleRoleChange">
            <el-option label="超级管理员" value="super_admin" />
            <el-option label="普通管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
          <div class="form-tip text-gray-400 text-xs mt-1">
             <div v-if="form.roles === 'super_admin'">拥有系统所有权限，无需分配茶园。</div>
             <div v-if="form.roles === 'admin'">管理指定的茶园及所属设备。</div>
             <div v-if="form.roles === 'user'">仅查看指定的茶园及所属设备。</div>
          </div>
        </el-form-item>
        
        <el-form-item label="分配茶园" v-if="form.roles !== 'super_admin'">
          <el-select v-model="form.garden_ids" multiple placeholder="请选择分配的茶园" style="width: 100%">
            <el-option
              v-for="item in gardenList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 移除复杂的功能权限勾选，改为由角色自动决定 -->

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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser, impersonateUser } from '@/api/user'
import { getTeaGardenList } from '@/api/tea-garden'

const router = useRouter()
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
  roles: 'user', // Default to single string
  garden_ids: [],
  permissions: []
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
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
    const res = await getTeaGardenList({ page: 1, size: 100 })
    gardenList.value = res.list || []
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
  // Convert roles array to single string for selector
  if (row.roles && row.roles.length > 0) {
      form.roles = row.roles[0]
  } else {
      form.roles = 'user'
  }
  form.password = ''
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

const handleImpersonate = (row) => {
  ElMessageBox.confirm(`确定要以 "${row.username}" 的身份登录系统吗？\n当前会话将结束。`, '身份切换', {
    confirmButtonText: '立即切换',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const res = await impersonateUser(row.id)
      if (res && res.token) {
          localStorage.setItem('tea_token', res.token)
          localStorage.setItem('tea_roles', JSON.stringify(res.userInfo.roles || []))
          localStorage.setItem('tea_permissions', JSON.stringify(res.userInfo.permissions || []))
          localStorage.setItem('tea_user', JSON.stringify(res.userInfo))
          
          ElMessage.success('身份切换成功，正在跳转...')
          setTimeout(() => {
              window.location.href = '/'
          }, 1000)
      }
    } catch (error) {
      console.error(error)
    }
  })
}

const handleRoleChange = (val) => {
    if (val === 'super_admin') {
        form.garden_ids = []
    }
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // Convert single role string back to array for backend
        const submission = {
            ...form,
            roles: [form.roles]
        }
        
        if (form.id) {
          const updateData = { ...submission }
          if (!updateData.password) delete updateData.password
          await updateUser(form.id, updateData)
          ElMessage.success('更新成功')
        } else {
          await createUser(submission)
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
  form.roles = 'user'
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
