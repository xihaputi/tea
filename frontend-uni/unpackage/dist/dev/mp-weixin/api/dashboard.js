"use strict";
const common_http = require("../common/http.js");
function getDashboardStats() {
  return common_http.api.get("/dashboard/stats");
}
exports.getDashboardStats = getDashboardStats;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/dashboard.js.map
