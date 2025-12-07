import request from '@/utils/request'

export function getRuleList(params) {
    return request({
        url: '/rules',
        method: 'get',
        params
    })
}

export function createRule(data) {
    return request({
        url: '/rules',
        method: 'post',
        data
    })
}

export function updateRule(id, data) {
    return request({
        url: `/rules/${id}`,
        method: 'put',
        data
    })
}

export function enableRule(id, enabled) {
    return request({
        url: `/rules/${id}/enable`,
        method: 'put',
        data: { enabled }
    })
}

export function deleteRule(id) {
    return request({
        url: `/rules/${id}`,
        method: 'delete'
    })
}

// Sensor Status Rule API
export function getSensorRules() {
    return request({
        url: '/rules/sensor',
        method: 'get'
    })
}

export function createSensorRule(data) {
    return request({
        url: '/rules/sensor',
        method: 'post',
        data
    })
}

export function updateSensorRule(id, data) {
    return request({
        url: `/rules/sensor/${id}`,
        method: 'put',
        data
    })
}

export function deleteSensorRule(id) {
    return request({
        url: `/rules/sensor/${id}`,
        method: 'delete'
    })
}

