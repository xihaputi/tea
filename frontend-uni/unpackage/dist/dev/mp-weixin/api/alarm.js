"use strict";
const common_http = require("../common/http.js");
function getAlarmList(params) {
  return common_http.api.get("/alarms", params);
}
function acknowledgeAlarm(id) {
  return common_http.api.put(`/alarms/${id}/ack`);
}
exports.acknowledgeAlarm = acknowledgeAlarm;
exports.getAlarmList = getAlarmList;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/alarm.js.map
