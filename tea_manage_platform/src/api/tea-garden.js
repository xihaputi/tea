import request from "@/utils/request"

// 茶园列表
export function getTeaGardenList(params) {
  return request({
    url: "/tea-gardens",
    method: "get",
    params,
  })
}

// 创建茶园
export function createTeaGarden(data) {
  return request({
    url: "/tea-gardens",
    method: "post",
    data,
  })
}

// 茶园详情
export function getTeaGardenDetail(id) {
  return request({
    url: `/tea-gardens/${id}`,
    method: "get",
  })
}

// 更新茶园
export function updateTeaGarden(id, data) {
  return request({
    url: `/tea-gardens/${id}`,
    method: "put",
    data,
  })
}

// 删除茶园
export function deleteTeaGarden(id) {
  return request({
    url: `/tea-gardens/${id}`,
    method: "delete",
  })
}

// 地块列表
export function getPlots(gardenId) {
  return request({
    url: `/tea-gardens/${gardenId}/plots`,
    method: "get",
  })
}

// 创建地块
export function createPlot(gardenId, data) {
  return request({
    url: `/tea-gardens/${gardenId}/plots`,
    method: "post",
    data,
  })
}

// 茶园下设备
export function getGardenDevices(gardenId) {
  return request({
    url: `/tea-gardens/${gardenId}/devices`,
    method: "get",
  })
}
