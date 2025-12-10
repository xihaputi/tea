"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  methods: {
    goChat() {
      common_vendor.index.navigateTo({ url: "/pages/chat/chat" });
    },
    goDisease() {
      common_vendor.index.navigateTo({ url: "/pages/disease/disease" });
    },
    showToast(msg) {
      common_vendor.index.showToast({ title: msg, icon: "none" });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.o((...args) => $options.goChat && $options.goChat(...args)),
    b: common_vendor.o((...args) => $options.goDisease && $options.goDisease(...args)),
    c: common_vendor.o(($event) => $options.showToast("即将上线"))
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-29b59d94"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/assistant/index.js.map
