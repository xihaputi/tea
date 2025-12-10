"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const common_vendor = require("./common/vendor.js");
if (!Math) {
  "./pages/index/index.js";
  "./pages/alarm/index.js";
  "./pages/plot/detail.js";
  "./pages/disease/disease.js";
  "./pages/chat/chat.js";
  "./pages/assistant/index.js";
  "./pages/profile/index.js";
  "./pages/plot/edit.js";
  "./pages/plot/index.js";
  "./pages/plot/edit_garden.js";
  "./pages/login/index.js";
}
const _sfc_main = {
  onLaunch() {
    common_vendor.index.__f__("log", "at App.vue:4", "App Launch");
    const token = common_vendor.index.getStorageSync("token");
    if (!token) {
      common_vendor.index.reLaunch({
        url: "/pages/login/index"
      });
    }
  },
  onShow() {
    common_vendor.index.__f__("log", "at App.vue:15", "App Show");
  },
  onHide() {
    common_vendor.index.__f__("log", "at App.vue:18", "App Hide");
  }
};
function createApp() {
  const app = common_vendor.createSSRApp(_sfc_main);
  app.config.globalProperties.$baseUrl = "http://116.62.25.191:1112/api";
  return { app };
}
createApp().app.mount("#app");
exports.createApp = createApp;
//# sourceMappingURL=../.sourcemap/mp-weixin/app.js.map
