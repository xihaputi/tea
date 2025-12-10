"use strict";
const common_vendor = require("../../common/vendor.js");
const api_auth = require("../../api/auth.js");
const _sfc_main = {
  data() {
    return {
      user: {}
    };
  },
  onShow() {
    this.loadUserInfo();
  },
  methods: {
    async loadUserInfo() {
      try {
        const res = await api_auth.getUserInfo();
        this.user = res;
      } catch (e) {
      }
    },
    async handleLogout() {
      try {
        await api_auth.logout();
      } catch (e) {
      }
      common_vendor.index.removeStorageSync("token");
      common_vendor.index.removeStorageSync("userInfo");
      common_vendor.index.reLaunch({ url: "/pages/login/index" });
    },
    showToast(msg) {
      common_vendor.index.showToast({ title: msg, icon: "none" });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($data.user.name ? $data.user.name[0] : $data.user.username ? $data.user.username[0] : "U"),
    b: common_vendor.t($data.user.name || $data.user.username),
    c: common_vendor.t($data.user.roles ? $data.user.roles.join(", ") : "普通用户"),
    d: common_vendor.o(($event) => $options.showToast("编辑功能开发中")),
    e: common_vendor.o(($event) => $options.showToast("账号安全功能开发中")),
    f: common_vendor.o(($event) => $options.showToast("系统设置功能开发中")),
    g: common_vendor.o(($event) => $options.showToast("关于我们功能开发中")),
    h: common_vendor.o((...args) => $options.handleLogout && $options.handleLogout(...args))
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-201c0da5"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/profile/index.js.map
