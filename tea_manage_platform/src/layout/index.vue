<template>
  <el-container class="h-screen">
    <el-aside width="240px" class="glass-aside">
      <div class="logo-area">
        <el-icon color="#13c2c2" size="24" class="mr-2"><Leaf /></el-icon>
        <span class="font-bold text-lg">Tea Brain</span>
      </div>
      <el-menu
        router
        :default-active="$route.path"
        class="border-none"
        text-color="#606266"
        active-text-color="#13c2c2"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon><span>运营总览</span>
        </el-menu-item>
        <el-menu-item index="/tea-garden/list">
          <el-icon><Collection /></el-icon><span>茶园管理</span>
        </el-menu-item>
        <el-menu-item index="/device/list">
          <el-icon><Cpu /></el-icon><span>设备管理</span>
        </el-menu-item>
        <el-menu-item index="/rule/index">
          <el-icon><Connection /></el-icon><span>规则配置</span>
        </el-menu-item>
        <el-menu-item index="/rule-engine/index">
          <el-icon><Cpu /></el-icon><span>规则引擎</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="glass-header">
        <div class="flex items-center text-gray-500">
          <el-icon class="mr-2"><Fold /></el-icon>
          <span>当前位置 / {{ $route.meta.title }}</span>
        </div>
        <div class="flex items-center">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="flex items-center cursor-pointer">
              <el-avatar :size="32" :src="userInfo.avatar || 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'" />
              <span class="ml-2 text-sm text-gray-600">{{ userInfo.name || '用户' }}</span>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>账号信息
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>

  <!-- 用户信息弹窗 -->
  <el-dialog v-model="profileVisible" title="账号信息" width="30%">
    <div class="profile-content">
      <div class="avatar-box">
        <el-avatar :size="80" :src="userInfo.avatar || 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'" />
      </div>
      <div class="info-item">
        <label>昵称：</label><span>{{ userInfo.name }}</span>
      </div>
      <div class="info-item">
        <label>角色：</label>
        <el-tag size="small" v-for="role in userInfo.roles" :key="role" class="mr-1">{{ role }}</el-tag>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserInfo, logout } from '@/api/auth'
import { User, SwitchButton, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userInfo = reactive({
  name: '',
  avatar: '',
  roles: []
})
const profileVisible = ref(false)

const fetchUserInfo = async () => {
  try {
    const res = await getUserInfo()
    if (res) {
      userInfo.name = res.name
      userInfo.avatar = res.avatar
      userInfo.roles = res.roles
    }
  } catch (error) {
    console.error('获取用户信息失败', error)
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    handleLogout()
  } else if (command === 'profile') {
    profileVisible.value = true
  }
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await logout()
    } catch (e) {
      console.error(e)
    } finally {
      localStorage.removeItem('tea_token')
      router.push('/login')
      ElMessage.success('已退出登录')
    }
  })
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.h-screen { height: 100vh; background-color: #f5f7fa; }
.glass-aside {
  background: #fff;
  border-right: 1px solid #f0f0f0;
  box-shadow: 4px 0 16px rgba(0,0,0,0.02);
  z-index: 20;
}
.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f5f5f5;
  color: #333;
}
:deep(.el-menu-item.is-active) {
  background-color: #e6fffb !important;
  border-right: 3px solid #13c2c2;
  color: #13c2c2;
  font-weight: 500;
}
.border-none { border: none; }
.glass-header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid #ebeef5;
}
.flex { display: flex; }
.items-center { align-items: center; }
.mr-2 { margin-right: 8px; }
.ml-2 { margin-left: 8px; }
.text-lg { font-size: 18px; }
.font-bold { font-weight: bold; }
.cursor-pointer { cursor: pointer; }
.profile-content {
  text-align: center;
  padding: 20px 0;
}
.avatar-box { margin-bottom: 20px; }
.info-item {
  margin-bottom: 12px;
  font-size: 16px;
  color: #606266;
}
.info-item label {
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}
</style>
