import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
    baseURL: '/api', // 所有的请求地址前缀部分
    timeout: 5000 // 请求超时时间
})

// request 拦截器
service.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么
        const token = localStorage.getItem('tea_token')
        if (token) {
            // 让每个请求携带自定义 token
            config.headers['Authorization'] = 'Bearer ' + token
        }
        return config
    },
    error => {
        // 对请求错误做些什么
        console.log(error)
        return Promise.reject(error)
    }
)

// response 拦截器
service.interceptors.response.use(
    response => {
        const res = response.data
        // 这里可以根据后端的通用状态码进行判断
        // 假设后端成功返回 code 为 200
        // 如果不是 200，则判断为错误
        // 注意：具体逻辑需要根据实际后端约定调整
        return res
    },
    error => {
        console.log('err' + error) // for debug
        ElMessage({
            message: error.message || '请求失败',
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }
)

export default service
