"use strict";
const common_http = require("../common/http.js");
function getSensorRules() {
  return common_http.api.get("/rules/sensor");
}
exports.getSensorRules = getSensorRules;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/rule.js.map
