<template>
  <div class="login-container">
    <div class="bg-layer"></div>
    <div class="login-card animate-up">
      <div class="header">
        <h1 class="app-name">Tea Brain</h1>
        <p class="app-slogan">注册账号</p>
      </div>

      <el-form class="login-form">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="账号 (必填)"
            prefix-icon="User"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="form.name"
            placeholder="姓名 (必填)"
            prefix-icon="Postcard"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码 (必填)"
            prefix-icon="Lock"
            show-password
            class="custom-input"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码 (必填)"
            prefix-icon="Lock"
            show-password
            class="custom-input"
          />
        </el-form-item>

        <el-button type="primary" class="login-btn" :loading="loading" @click="handleRegister">
          注册
        </el-button>

        <div class="footer-links">
          <span @click="$router.push('/login')">返回登录</span>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({ 
  username: '', 
  name: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (!form.username || !form.password || !form.name) {
    return ElMessage.warning('请填写完整信息')
  }
  if (form.password !== form.confirmPassword) {
    return ElMessage.warning('两次输入的密码不一致')
  }
  
  loading.value = true
  try {
    const res = await register({
      username: form.username,
      password: form.password,
      name: form.name
    })
    if (res && res.success) {
      ElMessage.success('注册成功')
      router.push('/login')
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 注册页面 */
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: #333;
}

.bg-layer {
  position: absolute;
  inset: 0;
  background: url('https://images.unsplash.com/photo-1586616863660-e4c163016259?q=80&w=2070&auto=format&fit=crop') no-repeat center center;
  background-size: cover;
  filter: blur(6px) brightness(0.85);
  transform: scale(1.05);
}

.login-card {
  position: relative;
  width: 380px;
  padding: 40px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.6);
  z-index: 10;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.app-name {
  font-size: 32px;
  font-weight: 800;
  color: #13c2c2;
  margin: 0;
  letter-spacing: -1px;
}

.app-slogan {
  font-size: 14px;
  color: #5c6b7f;
  margin-top: 5px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

:deep(.custom-input .el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: none;
  border-bottom: 2px solid transparent;
  border-radius: 8px;
  padding: 10px;
  transition: all 0.3s;
}

:deep(.custom-input .el-input__wrapper:hover),
:deep(.custom-input.is-focus .el-input__wrapper) {
  background-color: #fff;
  border-bottom: 2px solid #13c2c2;
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #42d392 0%, #13c2c2 100%);
  border: none;
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(19, 194, 194, 0.4);
  transition: all 0.3s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(19, 194, 194, 0.5);
}

.footer-links {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  font-size: 12px;
  color: #7d8592;
  cursor: pointer;
}

.animate-up {
  animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
