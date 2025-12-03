import request from "@/utils/request"

export function getProductGroups() {
  return request({ url: "/devices/products", method: "get" })
}

export function getDeviceList(params) {
  return request({ url: "/devices", method: "get", params })
}

export function createDevice(data) {
  return request({ url: "/devices", method: "post", data })
}

export function getDeviceDetail(id) {
  return request({ url: `/devices/${id}`, method: "get" })
}

export function getLatestTelemetry(id) {
  return request({ url: `/devices/${id}/telemetry`, method: "get" })
}

export function getHistoryTelemetry(id, params) {
  return request({ url: `/devices/${id}/telemetry/history`, method: "get", params })
}

export function updateDevice(id, data) {
  return request({ url: `/devices/${id}`, method: "put", data })
}

// HTTP 上报遥测
export function postTelemetry(id, data) {
  return request({ url: `/devices/${id}/telemetry`, method: "post", data })
}

export function deleteDevice(id) {
  return request({ url: `/devices/${id}`, method: "delete" })
}
