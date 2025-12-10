"use strict";
const common_http = require("../common/http.js");
function detectDisease(filePath, plotId) {
  return common_http.api.upload("/disease/detect", filePath, "file", {
    "plot_id": plotId || ""
  });
}
exports.detectDisease = detectDisease;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/disease.js.map
