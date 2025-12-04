import request from "@/utils/request"

export function getAlarmList(params) {
    return request({ url: "/alarms", method: "get", params })
}

export function acknowledgeAlarm(id) {
    return request({ url: `/alarms/${id}/ack`, method: "put" })
}

export function clearAlarm(id) {
    return request({ url: `/alarms/${id}/clear`, method: "put" })
}
