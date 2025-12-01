import request from '@/utils/request'

// 获取验证码
// Get captcha
export function getCaptcha() {
    return request({
        url: '/auth/captcha',
        method: 'get'
    })
}

// 用户登录
// User login
export function login(data) {
    return request({
        url: '/auth/login',
        method: 'post',
        data
    })
}

// 用户注册
// User registration
export function register(data) {
    return request({
        url: '/auth/register',
        method: 'post',
        data
    })
}

// 重置密码
// Reset password
export function resetPassword(data) {
    return request({
        url: '/auth/reset-password',
        method: 'post',
        data
    })
}

// 获取用户信息
// Get user info
export function getUserInfo() {
    return request({
        url: '/auth/user/info',
        method: 'get'
    })
}

// 退出登录
// Logout
export function logout() {
    return request({
        url: '/auth/logout',
        method: 'post'
    })
}
