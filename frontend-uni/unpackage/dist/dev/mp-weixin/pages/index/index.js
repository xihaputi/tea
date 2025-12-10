"use strict";
const common_vendor = require("../../common/vendor.js");
const api_dashboard = require("../../api/dashboard.js");
const api_garden = require("../../api/garden.js");
const _sfc_main = {
  data() {
    return {
      stats: {
        garden_count: 0,
        device_online_count: 0,
        alarm_count: 0
      },
      gardens: [],
      loading: false,
      userName: "管理员"
    };
  },
  onShow() {
    const userInfo = common_vendor.index.getStorageSync("userInfo");
    if (userInfo && (userInfo.name || userInfo.username)) {
      this.userName = userInfo.name || userInfo.username;
    }
    this.loadData();
  },
  onPullDownRefresh() {
    this.loadData();
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const [statsRes, gardensRes] = await Promise.all([
          api_dashboard.getDashboardStats(),
          api_garden.getGardenList({ page: 1, size: 100 })
        ]);
        this.stats = statsRes;
        this.gardens = gardensRes.list.map((item) => ({
          ...item,
          devices: item.totalCount || 0,
          image: item.image_path ? this.$baseUrl + item.image_path : "/static/default_garden.jpg",
          // Handle image path
          lastAlert: item.alarmCount > 0 ? `${item.alarmCount}条告警待处理` : null
        }));
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/index/index.vue:115", e);
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      } finally {
        this.loading = false;
        common_vendor.index.stopPullDownRefresh();
      }
    },
    goDetail(id) {
      common_vendor.index.navigateTo({ url: `/pages/plot/index?garden_id=${id}` });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($data.userName),
    b: common_vendor.t($data.stats.garden_count),
    c: common_vendor.t($data.stats.device_online_count),
    d: common_vendor.t($data.stats.alarm_count),
    e: $data.stats.alarm_count > 0 ? 1 : "",
    f: common_vendor.f($data.gardens, (item, k0, i0) => {
      return common_vendor.e({
        a: item.image,
        b: common_vendor.t(item.name),
        c: common_vendor.t(item.status === "normal" ? "正常运行" : "需关注"),
        d: common_vendor.n(item.status === "normal" ? "tag-primary" : "tag-warn"),
        e: common_vendor.t(item.area),
        f: common_vendor.t(item.devices),
        g: item.lastAlert
      }, item.lastAlert ? {
        h: common_vendor.t(item.lastAlert)
      } : {}, {
        i: item.id,
        j: common_vendor.o(($event) => $options.goDetail(item.id), item.id)
      });
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-1cf27b2a"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/index/index.js.map
