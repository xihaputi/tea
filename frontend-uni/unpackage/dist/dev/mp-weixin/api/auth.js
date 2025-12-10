"use strict";
const common_http = require("../common/http.js");
function login(data) {
  return common_http.api.post("/auth/login", data);
}
function getUserInfo() {
  return common_http.api.get("/auth/user/info");
}
function logout() {
  return common_http.api.post("/auth/logout");
}
exports.getUserInfo = getUserInfo;
exports.login = login;
exports.logout = logout;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/auth.js.map
