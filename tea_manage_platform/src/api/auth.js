import request from '@/utils/request'

export function getCaptcha() {
    return request({
        url: '/auth/captcha',
        method: 'get'
    })
}

export function login(data) {
    return request({
        url: '/auth/login',
        method: 'post',
        data
    })
}

export function register(data) {
    return request({
        url: '/auth/register',
        method: 'post',
        data
    })
}

export function resetPassword(data) {
    return request({
        url: '/auth/reset-password',
        method: 'post',
        data
    })
}

export function getUserInfo() {
    return request({
        url: '/auth/user/info',
        method: 'get'
    })
}

export function logout() {
    return request({
        url: '/auth/logout',
        method: 'post'
    })
}
