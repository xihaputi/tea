"use strict";const t=require("../common/http.js");exports.acknowledgeAlarm=function(r){return t.api.put(`/alarms/${r}/ack`)},exports.getAlarmList=function(r){return t.api.get("/alarms",r)};
