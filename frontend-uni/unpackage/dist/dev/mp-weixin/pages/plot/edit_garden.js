"use strict";
const common_vendor = require("../../common/vendor.js");
const api_garden = require("../../api/garden.js");
const common_http = require("../../common/http.js");
const _sfc_main = {
  data() {
    return {
      gardenId: null,
      form: {
        name: "",
        description: "",
        address: "",
        image_path: ""
      },
      saving: false,
      showCoverSelector: false
    };
  },
  computed: {
    coverUrl() {
      if (!this.form.image_path)
        return "/static/gardens/1.png";
      if (this.form.image_path.startsWith("http"))
        return this.form.image_path;
      const base = this.$baseUrl || "";
      return base + this.form.image_path;
    }
  },
  onLoad(options) {
    if (options.id) {
      this.gardenId = Number(options.id);
      this.loadData();
    }
  },
  methods: {
    async loadData() {
      try {
        const res = await api_garden.getGardenDetail(this.gardenId);
        this.form = {
          name: res.name,
          description: res.description,
          address: res.address,
          image_path: res.image_path
        };
      } catch (e) {
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      }
    },
    selectSystemImage(index) {
      this.form.image_path = `/static/gardens/${index}.png`;
      this.showCoverSelector = false;
    },
    chooseImage() {
      common_vendor.index.chooseImage({
        count: 1,
        success: async (res) => {
          const filePath = res.tempFilePaths[0];
          try {
            common_vendor.index.showLoading({ title: "上传中" });
            const uploadRes = await common_http.api.upload("/upload/file", filePath, "file");
            this.form.image_path = uploadRes.url || uploadRes.path;
            this.showCoverSelector = false;
          } catch (e) {
            common_vendor.index.showToast({ title: "上传失败", icon: "none" });
          } finally {
            common_vendor.index.hideLoading();
          }
        }
      });
    },
    async save() {
      this.saving = true;
      try {
        await api_garden.updateGarden(this.gardenId, this.form);
        common_vendor.index.showToast({ title: "保存成功", icon: "success" });
        setTimeout(() => {
          const pages = getCurrentPages();
          const prevPage = pages[pages.length - 2];
          if (prevPage && prevPage.$vm.loadData) {
            prevPage.$vm.loadData();
          }
          common_vendor.index.navigateBack();
        }, 1500);
      } catch (e) {
        common_vendor.index.showToast({ title: "保存失败", icon: "none" });
      } finally {
        this.saving = false;
      }
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.form.name,
    b: common_vendor.o(($event) => $data.form.name = $event.detail.value),
    c: $options.coverUrl,
    d: common_vendor.o(($event) => $data.showCoverSelector = true),
    e: $data.form.description,
    f: common_vendor.o(($event) => $data.form.description = $event.detail.value),
    g: $data.form.address,
    h: common_vendor.o(($event) => $data.form.address = $event.detail.value),
    i: common_vendor.o((...args) => $options.save && $options.save(...args)),
    j: $data.saving,
    k: $data.showCoverSelector
  }, $data.showCoverSelector ? {
    l: common_vendor.o(($event) => $data.showCoverSelector = false),
    m: common_vendor.o((...args) => $options.chooseImage && $options.chooseImage(...args)),
    n: common_vendor.f(14, (i, k0, i0) => {
      return common_vendor.e({
        a: `${_ctx.$baseUrl}/static/gardens/${i}.png`,
        b: $data.form.image_path === `/static/gardens/${i}.png`
      }, $data.form.image_path === `/static/gardens/${i}.png` ? {} : {}, {
        c: i,
        d: $data.form.image_path === `/static/gardens/${i}.png` ? 1 : "",
        e: common_vendor.o(($event) => $options.selectSystemImage(i), i)
      });
    }),
    o: common_vendor.o(() => {
    }),
    p: common_vendor.o(($event) => $data.showCoverSelector = false)
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-8b8cee47"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/plot/edit_garden.js.map
