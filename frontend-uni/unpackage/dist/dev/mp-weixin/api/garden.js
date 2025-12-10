"use strict";
const common_http = require("../common/http.js");
function getGardenList(params) {
  return common_http.api.get("/tea-gardens", params);
}
function getGardenDetail(id) {
  return common_http.api.get(`/tea-gardens/${id}`);
}
function getGardenDevices(gardenId) {
  return common_http.api.get(`/tea-gardens/${gardenId}/devices`);
}
function updateGarden(id, data) {
  return common_http.api.put(`/tea-gardens/${id}`, data);
}
exports.getGardenDetail = getGardenDetail;
exports.getGardenDevices = getGardenDevices;
exports.getGardenList = getGardenList;
exports.updateGarden = updateGarden;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/garden.js.map
