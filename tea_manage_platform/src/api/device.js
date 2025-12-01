import request from '@/utils/request'

// 获取产品分组（设备类型）
// Get product groups (device types)
export function getProductGroups() {
    return request({
        url: '/devices/products',
        method: 'get'
    })
}

// 获取设备列表
// Get device list
export function getDeviceList(params) {
    return request({
        url: '/devices',
        method: 'get',
        params
    })
}

// 创建设备
// Create device
export function createDevice(data) {
    return request({
        url: '/devices',
        method: 'post',
        data
    })
}

// 获取设备详情
// Get device details
export function getDeviceDetail(id) {
    return request({
        url: `/devices/${id}`,
        method: 'get'
    })
}

// 获取最新遥测数据
// Get latest telemetry data
export function getLatestTelemetry(id) {
    return request({
        url: `/devices/${id}/telemetry`,
        method: 'get'
    })
}

// 获取历史遥测数据
// Get historical telemetry data
export function getHistoryTelemetry(id, params) {
    return request({
        url: `/devices/${id}/telemetry/history`,
        method: 'get',
        params
    })
}

// 更新设备信息
// Update device information
export function updateDevice(id, data) {
    return request({
        url: `/devices/${id}`,
        method: 'put',
        data
    })
}
