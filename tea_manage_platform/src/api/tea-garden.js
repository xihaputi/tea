
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
