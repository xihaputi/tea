"use strict";
const common_vendor = require("./vendor.js");
const BASE_URL = process.env.UNI_APP_API_BASE || "http://116.62.25.191:1112/api";
const request = (method, url, data = {}) => new Promise((resolve, reject) => {
  const token = common_vendor.index.getStorageSync("token");
  const header = {};
  if (token) {
    header["Authorization"] = token;
  }
  common_vendor.index.request({
    url: `${BASE_URL}${url}`,
    method,
    data,
    header,
    success: (res) => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        resolve(res.data);
      } else if (res.statusCode === 401) {
        common_vendor.index.removeStorageSync("token");
        common_vendor.index.showToast({ title: "���ȵ�¼", icon: "none" });
        reject(res);
      } else {
        reject(res);
      }
    },
    fail: reject
  });
});
const upload = (url, filePath, name = "file", formData = {}) => new Promise((resolve, reject) => {
  const token = common_vendor.index.getStorageSync("token");
  const header = {};
  if (token) {
    header["Authorization"] = token;
  }
  common_vendor.index.uploadFile({
    url: `${BASE_URL}${url}`,
    filePath,
    name,
    formData,
    header,
    success: (res) => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        resolve(JSON.parse(res.data));
      } else {
        reject(res);
      }
    },
    fail: reject
  });
});
const api = {
  get: (url, data) => request("GET", url, data),
  post: (url, data) => request("POST", url, data),
  put: (url, data) => request("PUT", url, data),
  delete: (url, data) => request("DELETE", url, data),
  upload
};
exports.api = api;
//# sourceMappingURL=../../.sourcemap/mp-weixin/common/http.js.map
