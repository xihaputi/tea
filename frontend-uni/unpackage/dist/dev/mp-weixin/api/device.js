"use strict";
const common_http = require("../common/http.js");
function getLatestTelemetry(deviceId) {
  return common_http.api.get(`/devices/${deviceId}/telemetry`);
}
exports.getLatestTelemetry = getLatestTelemetry;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/device.js.map
