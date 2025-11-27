import request from '@/utils/request'

// 茶园相关
export function getTeaGardenList(params) {
    return request({
        url: '/tea-gardens',
        method: 'get',
        params
    })
}

export function getTeaGardenDetail(id) {
    return request({
        url: `/tea-gardens/${id}`,
        method: 'get'
    })
}

export function createTeaGarden(data) {
    return request({
        url: '/tea-gardens',
        method: 'post',
        data
    })
}

export function updateTeaGarden(id, data) {
    return request({
        url: `/tea-gardens/${id}`,
        method: 'put',
        data
    })
}

export function deleteTeaGarden(id) {
    return request({
        url: `/tea-gardens/${id}`,
        method: 'delete'
    })
}

// 地块相关
export function getPlots(gardenId) {
    return request({
        url: `/tea-gardens/${gardenId}/plots`,
        method: 'get'
    })
}

export function createPlot(gardenId, data) {
    return request({
        url: `/tea-gardens/${gardenId}/plots`,
        method: 'post',
        data
    })
}

// 关联设备
export function getGardenDevices(gardenId) {
    return request({
        url: `/tea-gardens/${gardenId}/devices`,
        method: 'get'
    })
}
