"use strict";
const common_vendor = require("../../common/vendor.js");
const api_disease = require("../../api/disease.js");
const _sfc_main = {
  data() {
    return {
      filePath: "",
      result: null,
      uploading: false,
      error: ""
    };
  },
  methods: {
    chooseImage() {
      common_vendor.index.chooseImage({
        count: 1,
        sizeType: ["compressed"],
        success: (res) => {
          this.filePath = res.tempFilePaths[0];
          this.result = null;
          this.error = "";
        },
        fail: () => {
        }
      });
    },
    async upload() {
      if (!this.filePath)
        return;
      this.uploading = true;
      this.error = "";
      try {
        const res = await api_disease.detectDisease(this.filePath);
        this.result = res;
      } catch (e) {
        this.error = "识别失败，请检查网络或重试";
      } finally {
        this.uploading = false;
      }
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.filePath
  }, $data.filePath ? {
    b: $data.filePath
  } : {}, {
    c: common_vendor.o((...args) => $options.chooseImage && $options.chooseImage(...args)),
    d: $data.filePath && !$data.uploading && !$data.result
  }, $data.filePath && !$data.uploading && !$data.result ? {
    e: common_vendor.o((...args) => $options.upload && $options.upload(...args))
  } : {}, {
    f: $data.uploading
  }, $data.uploading ? {} : {}, {
    g: $data.result
  }, $data.result ? {
    h: common_vendor.t(($data.result.confidence * 100).toFixed(1)),
    i: common_vendor.t($data.result.disease_type),
    j: common_vendor.t($data.result.advice)
  } : {}, {
    k: $data.error
  }, $data.error ? {
    l: common_vendor.t($data.error)
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-0a006d31"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/disease/disease.js.map
