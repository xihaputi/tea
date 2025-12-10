<template>
  <div class="login-container">
    <div class="bg-layer"></div>
    <div class="login-card animate-up">
      <div class="header">
        <img src="@/assets/logo.jpg" alt="Logo" class="logo-img" />
        <h1 class="app-name">茶智云</h1>
        <p class="app-slogan">智慧茶园数字大脑</p>
      </div>

      <el-form class="login-form">
        <el-form-item>
          <el-input v-model="form.username" placeholder="请输入账号" prefix-icon="User" class="custom-input" />
        </el-form-item>

        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password class="custom-input" />
        </el-form-item>

        <el-button type="primary" class="login-btn" :loading="loading" @click="handleLogin">
          立即进入
          <el-icon class="ml-2"><ArrowRight /></el-icon>
        </el-button>

        <div class="footer-links">
          <span class="link-text" @click="$router.push('/login/forget')">忘记密码</span>
          <span class="link-divider">|</span>
          <span class="link-text" @click="$router.push('/login/register')">注册账号</span>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login as apiLogin } from '@/api/auth'
import { User, Lock, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('请输入账号和密码')
  }
  loading.value = true
  try {
    const res = await apiLogin({ username: form.username, password: form.password })
    console.log('Login response:', res) 
    if (res && res.token) {
      localStorage.setItem('tea_token', res.token)
      localStorage.setItem('tea_roles', JSON.stringify(res.userInfo?.roles || []))
      localStorage.setItem('tea_permissions', JSON.stringify(res.userInfo?.permissions || []))
      localStorage.setItem('tea_user', JSON.stringify(res.userInfo || {}))

      ElMessage.success('登录成功')
      router.push('/dashboard')
    } else {
      console.error('Invalid login response:', res)
      ElMessage.error('登录失败：无效的响应格式')
    }
  } catch (error) {
    console.error('Login error:', error)
    ElMessage.error(error?.response?.data?.detail || '登录失败，请检查账号密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>

.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: #1a202c; /* Fallback */
}

.bg-layer {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(19, 194, 194, 0.2) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(66, 211, 146, 0.15) 0%, transparent 40%),
    linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  z-index: 0;
}

/* 动态光斑动画 */
.bg-layer::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.03) 0%, transparent 50%);
  animation: rotate 60s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.login-card {
  position: relative;
  width: 420px;
  padding: 56px 48px;
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
  z-index: 10;
  display: flex;
  flex-direction: column;
}

.header { text-align: center; margin-bottom: 40px; }
.logo-img { 
  width: 80px; 
  height: 80px; 
  border-radius: 20px; 
  margin-bottom: 20px; 
  box-shadow: 0 12px 24px rgba(19, 194, 194, 0.2);
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.logo-img:hover { transform: scale(1.1) rotate(5deg); }

.app-name { 
  font-size: 32px; 
  font-weight: 900; 
  color: #0f172a; 
  margin: 0; 
  letter-spacing: -0.5px;
  background: linear-gradient(to right, #13c2c2, #42d392);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.app-slogan { 
  font-size: 14px; 
  color: #64748b; 
  margin-top: 8px; 
  letter-spacing: 3px; 
  text-transform: uppercase; 
  font-weight: 500;
}

:deep(.custom-input .el-input__wrapper) {
  background-color: rgba(241, 245, 249, 0.8);
  box-shadow: none !important;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 8px 12px;
  height: 46px;
  transition: all 0.3s ease;
}
:deep(.custom-input .el-input__wrapper:hover) {
  background-color: #fff;
  border-color: #e2e8f0;
}
:deep(.custom-input.is-focus .el-input__wrapper) {
  background-color: #fff;
  border-color: #13c2c2;
  box-shadow: 0 0 0 4px rgba(19, 194, 194, 0.1) !important;
}

.login-btn {
  width: 100%;
  height: 50px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #42d392 0%, #13c2c2 100%);
  border: none;
  margin-top: 16px;
  box-shadow: 0 10px 20px -5px rgba(19, 194, 194, 0.4);
  transition: all 0.3s;
}
.login-btn:hover { 
  transform: translateY(-2px); 
  box-shadow: 0 15px 25px -5px rgba(19, 194, 194, 0.5); 
}
.login-btn:active { transform: translateY(0); }

.footer-links { 
  margin-top: 24px; 
  display: flex; 
  justify-content: center; 
  align-items: center;
  font-size: 14px; 
  color: #94a3b8; 
}
.link-text {
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.3s;
}
.link-text:hover { color: #13c2c2; }
.link-divider { margin: 0 12px; color: #cbd5e1; }

.ml-2 { margin-left: 8px; }
.animate-up { animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1); }
@keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
</style>
