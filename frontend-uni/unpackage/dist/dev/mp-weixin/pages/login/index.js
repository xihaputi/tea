"use strict";
const common_vendor = require("../../common/vendor.js");
const api_auth = require("../../api/auth.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        common_vendor.index.showToast({ title: "请输入账号和密码", icon: "none" });
        return;
      }
      this.loading = true;
      try {
        const res = await api_auth.login(this.form);
        common_vendor.index.setStorageSync("token", res.token);
        common_vendor.index.setStorageSync("userInfo", res.userInfo);
        common_vendor.index.setStorageSync("roles", res.userInfo.roles || []);
        common_vendor.index.showToast({ title: "登录成功", icon: "success" });
        setTimeout(() => {
          common_vendor.index.reLaunch({ url: "/pages/index/index" });
        }, 1500);
      } catch (e) {
        common_vendor.index.showToast({ title: e.detail || "登录失败", icon: "none" });
      } finally {
        this.loading = false;
      }
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_assets._imports_0$1,
    b: $data.form.username,
    c: common_vendor.o(($event) => $data.form.username = $event.detail.value),
    d: $data.form.password,
    e: common_vendor.o(($event) => $data.form.password = $event.detail.value),
    f: common_vendor.o((...args) => $options.handleLogin && $options.handleLogin(...args)),
    g: $data.loading
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-d08ef7d4"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/login/index.js.map
