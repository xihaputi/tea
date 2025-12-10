"use strict";const e=require("../common/http.js");exports.getLatestTelemetry=function(t){return e.api.get(`/devices/${t}/telemetry`)};
