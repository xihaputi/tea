<template>
  <el-container class="h-screen">
    <el-aside :width="asideWidth" class="glass-aside transition-all duration-300">
      <div class="logo-area">
        <el-icon color="#13c2c2" size="24" class="mr-2"><Leaf /></el-icon>
        <span class="font-bold text-lg" v-show="!isCollapse">Tea Brain</span>
      </div>
      <el-menu
        router
        :default-active="$route.path"
        class="border-none"
        text-color="#606266"
        active-text-color="#13c2c2"
        :collapse="isCollapse"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon><template #title>运营总览</template>
        </el-menu-item>
        <el-menu-item index="/tea-garden/list">
          <el-icon><Collection /></el-icon><template #title>茶园管理</template>
        </el-menu-item>
        <el-menu-item index="/device/list">
          <el-icon><Cpu /></el-icon><template #title>设备管理</template>
        </el-menu-item>
        <el-menu-item index="/rule/index">
          <el-icon><Connection /></el-icon><template #title>规则配置</template>
        </el-menu-item>
        <el-menu-item index="/alarm/index">
          <el-icon><Bell /></el-icon>
          <template #title>
            <span>告警记录</span>
            <span v-if="activeAlarmCount > 0" class="alarm-dot"></span>
          </template>
        </el-menu-item>
        <el-menu-item index="/task/index">
          <el-icon><Timer /></el-icon><template #title>计划任务</template>
        </el-menu-item>

        
        <el-sub-menu index="/system" v-if="userInfo.roles.includes('admin') || userInfo.roles.includes('super_admin')">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/system/user">用户管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="glass-header">
        <div class="flex items-center text-gray-500">
          <el-icon class="mr-2 cursor-pointer hover:text-primary" size="20" @click="toggleCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
          <span>当前位置 / {{ $route.meta.title }}</span>
        </div>
        <div class="flex items-center">
          <!-- 通知 -->
          <div class="mr-4 cursor-pointer hover:text-primary">
            <el-popover
              placement="bottom"
              :width="300"
              trigger="click"
              popper-class="notification-popover"
              @show="fetchNotifications"
            >
              <template #reference>
                <el-badge :value="activeAlarmCount" :hidden="activeAlarmCount === 0" class="item" type="danger">
                  <el-icon size="20"><Bell /></el-icon>
                </el-badge>
              </template>
              
              <div class="notification-list">
                <div class="notification-header">
                  <span>最新告警</span>
                  <el-link type="primary" :underline="false" @click="router.push('/alarm/index')">查看全部</el-link>
                </div>
                <div v-if="notificationList.length === 0" class="empty-notification">
                  <el-icon size="30" color="#909399"><CircleCheck /></el-icon>
                  <p>暂无未处理告警</p>
                </div>
                <div 
                  v-else 
                  v-for="item in notificationList" 
                  :key="item.id" 
                  class="notification-item"
                  @click="handleNotificationClick(item)"
                >
                  <div class="notification-icon">
                    <el-icon color="#f56c6c"><Warning /></el-icon>
                  </div>
                  <div class="notification-content">
                    <div class="notification-title">{{ item.content }}</div>
                    <div class="notification-time">{{ item.created_at }}</div>
                  </div>
                </div>
              </div>
            </el-popover>
          </div>
          <!-- 主题 -->
          <el-dropdown class="mr-4" trigger="click" @command="toggleTheme">
             <div class="cursor-pointer hover:text-primary flex items-center">
                <el-icon size="20"><MagicStick /></el-icon>
             </div>
             <template #dropdown>
               <el-dropdown-menu>
                 <el-dropdown-item :disabled="!isDark" command="light">默认主题</el-dropdown-item>
                 <el-dropdown-item :disabled="isDark" command="dark">暗黑模式</el-dropdown-item>
               </el-dropdown-menu>
             </template>
          </el-dropdown>
          
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
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
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
import { ref, onMounted, onUnmounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { getUserInfo, logout } from '@/api/auth'
import { getDashboardStats } from '@/api/dashboard'
import { getAlarmList } from '@/api/alarm'
import { User, SwitchButton, ArrowDown, Bell, Expand, Fold, MagicStick, Setting, Warning, CircleCheck, Timer } from '@element-plus/icons-vue'

const router = useRouter()
const isCollapse = ref(false)

// 用户信息响应式对象
// User info reactive object
const userInfo = reactive({
  name: '',
  avatar: '',
  roles: []
})
const profileVisible = ref(false)

const asideWidth = computed(() => isCollapse.value ? '64px' : '240px')

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  const html = document.documentElement
  if (isDark.value) {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
}

// 获取用户信息
// Fetch user info
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

// 全局告警轮询
// Global alarm polling
const activeAlarmCount = ref(0)
let alarmTimer = null
const notificationList = ref([])

const pollAlarms = async () => {
  try {
    const res = await getDashboardStats()
    const newCount = res.alarm_count
    
    // 如果告警数增加，显示通知
    // If alarm count increases, show notification
    if (newCount > activeAlarmCount.value && activeAlarmCount.value !== 0) {
      ElNotification({
        title: '新告警提醒',
        message: `检测到 ${newCount - activeAlarmCount.value} 条新的活动告警，请及时处理！`,
        type: 'error',
        duration: 5000
      })
      // 刷新通知列表
      fetchNotifications()
    }
    
    activeAlarmCount.value = newCount
  } catch (error) {
    console.error('Polling alarms failed', error)
  }
}

// 获取最新通知（告警）
const fetchNotifications = async () => {
  try {
    const res = await getAlarmList({ page: 1, size: 5, status: 'active' })
    notificationList.value = res.list
  } catch (error) {
    console.error(error)
  }
}

const handleNotificationClick = (item) => {
  router.push('/alarm/index')
}

// 处理下拉菜单命令
// Handle dropdown commands
const handleCommand = (command) => {
  if (command === 'logout') {
    handleLogout()
  } else if (command === 'profile') {
    profileVisible.value = true
  }
}

// 处理退出登录
// Handle logout
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
      // 清除 Token 并跳转到登录页
      // Clear token and redirect to login
      localStorage.removeItem('tea_token')
      router.push('/login')
      ElMessage.success('已退出登录')
    }
  })
}

onMounted(() => {
  fetchUserInfo()
  // 立即执行一次，然后每5秒轮询
  pollAlarms()
  fetchNotifications()
  alarmTimer = setInterval(pollAlarms, 5000)
})

onUnmounted(() => {
  if (alarmTimer) clearInterval(alarmTimer)
})
</script>

<style scoped>
.h-screen { height: 100vh; background-color: #f5f7fa; }
.glass-aside {
  background: #fff;
  border-right: 1px solid #f0f0f0;
  box-shadow: 4px 0 16px rgba(0,0,0,0.02);
  z-index: 20;
  transition: width 0.3s ease-in-out; /* 侧边栏宽度过渡动画 */
}
.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f5f5f5;
  color: #333;
  overflow: hidden; /* 防止收起时文字溢出 */
  white-space: nowrap;
}
:deep(.el-menu) {
  border-right: none;
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
.mr-4 { margin-right: 24px; } /* 增加右侧图标间距 */
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

/* 页面切换动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}
.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 暗黑模式样式 */
:global(.dark) .h-screen { background-color: #121212; }
:global(.dark) .glass-aside {
  background: #1d1e1f;
  border-right: 1px solid #363637;
}
:global(.dark) .logo-area {
  border-bottom: 1px solid #363637;
  color: #e5eaf3;
}
:global(.dark) .glass-header {
  background: rgba(29, 30, 31, 0.85);
  border-bottom: 1px solid #363637;
}
:global(.dark) :deep(.el-menu) {
  background-color: #1d1e1f;
}
:global(.dark) :deep(.el-menu-item) {
  color: #e5eaf3;
}
:global(.dark) :deep(.el-menu-item:hover) {
  background-color: #262727;
}
:global(.dark) :deep(.el-menu-item.is-active) {
  background-color: #132222 !important;
  color: #13c2c2;
}
:global(.dark) .text-gray-500,
:global(.dark) .text-gray-600 {
  color: #a3a6ad;
}
.alarm-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #f56c6c;
  border-radius: 50%;
  margin-left: 8px;
  position: relative;
  top: -1px;
}

/* 通知列表样式 */
.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 8px;
  font-weight: bold;
  color: #303133;
}
.empty-notification {
  text-align: center;
  padding: 24px 0;
  color: #909399;
}
.empty-notification p {
  margin-top: 8px;
  font-size: 13px;
}
.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}
.notification-item:hover {
  background-color: #f5f7fa;
}
.notification-icon {
  margin-right: 12px;
  margin-top: 2px;
}
.notification-content {
  flex: 1;
}
.notification-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  line-height: 1.4;
}
.notification-time {
  font-size: 12px;
  color: #909399;
}

:global(.dark) .notification-header {
  border-bottom-color: #363637;
  color: #e5eaf3;
}
:global(.dark) .notification-item:hover {
  background-color: #262727;
}
:global(.dark) .notification-title {
  color: #e5eaf3;
}
</style>
