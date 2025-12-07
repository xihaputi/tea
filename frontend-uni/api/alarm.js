import { api } from '@/common/http.js';

export function getAlarmList(params) {
    return api.get('/alarms', params);
}

export function getAlarmDetail(id) {
    return api.get(`/alarms/${id}`);
}

export function acknowledgeAlarm(id) {
    return api.put(`/alarms/${id}/ack`);
}

export function clearAlarm(id) {
    return api.put(`/alarms/${id}/clear`);
}
