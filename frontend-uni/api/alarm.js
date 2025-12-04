import { api } from '@/common/http.js';

export function getAlarmList(params) {
    return api.get('/alarms', params);
}

export function getAlarmDetail(id) {
    return api.get(`/alarms/${id}`);
}

export function updateAlarmStatus(id, status) {
    return api.put(`/alarms/${id}/status`, { status });
}
