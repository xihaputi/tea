"use strict";
const common_http = require("../../common/http.js");
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      plotId: null,
      sensor: null,
      advice: null,
      loading: false,
      error: ""
    };
  },
  onLoad(options) {
    this.plotId = Number(options.plot_id);
    this.refresh();
  },
  methods: {
    async refresh() {
      if (!this.plotId) {
        this.error = "未传递地块 ID";
        return;
      }
      this.loading = true;
      this.error = "";
      try {
        const [sensor, advice] = await Promise.all([
          common_http.api.get("/sensor/latest", { plot_id: this.plotId }),
          common_http.api.get("/advice/today", { plot_id: this.plotId })
        ]);
        this.sensor = sensor;
        this.advice = advice;
      } catch (e) {
        this.error = "加载失败，请检查后端服务";
      } finally {
        this.loading = false;
      }
    },
    formatTime(ts) {
      if (!ts)
        return "--";
      return ts.replace("T", " ").replace("Z", "");
    },
    pillClass(level) {
      if (level === "optimal")
        return "pill-optimal";
      if (level === "water")
        return "pill-water";
      if (level === "drain")
        return "pill-drain";
      return "pill-optimal";
    },
    adviceText(level) {
      if (level === "optimal")
        return "适宜";
      if (level === "water")
        return "建议浇水";
      if (level === "drain")
        return "注意排水";
      return level || "未知";
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.t($data.plotId),
    b: $data.error
  }, $data.error ? {
    c: common_vendor.t($data.error)
  } : {}, {
    d: $data.loading
  }, $data.loading ? {} : {}, {
    e: $data.sensor
  }, $data.sensor ? {
    f: common_vendor.t($options.formatTime($data.sensor.timestamp)),
    g: common_vendor.t($data.sensor.soil_moisture),
    h: common_vendor.t($data.sensor.temperature || "--"),
    i: common_vendor.t($data.sensor.humidity || "--")
  } : {}, {
    j: $data.advice
  }, $data.advice ? {
    k: common_vendor.t($options.adviceText($data.advice.level)),
    l: common_vendor.n($options.pillClass($data.advice.level)),
    m: common_vendor.t($data.advice.advice),
    n: common_vendor.t($options.formatTime($data.advice.timestamp))
  } : {}, {
    o: common_vendor.o((...args) => $options.refresh && $options.refresh(...args))
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-614075fc"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/plot/detail.js.map
