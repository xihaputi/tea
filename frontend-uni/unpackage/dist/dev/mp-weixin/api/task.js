"use strict";
const common_http = require("../common/http.js");
function getTaskList(params) {
  return common_http.api.get("/tasks/", params);
}
function updateTask(id, data) {
  return common_http.api.put(`/tasks/${id}`, data);
}
exports.getTaskList = getTaskList;
exports.updateTask = updateTask;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/task.js.map
