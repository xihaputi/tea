import { api } from '@/common/http.js';

// 获取设备最新遥测数据
export function getLatestTelemetry(deviceId) {
    return api.get(`/devices/${deviceId}/telemetry`);
}
