"use strict";
const common_vendor = require("../../common/vendor.js");
const api_garden = require("../../api/garden.js");
const api_device = require("../../api/device.js");
const api_rule = require("../../api/rule.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      gardenId: null,
      garden: {},
      devices: [],
      loading: false,
      lastUpdated: "",
      rulesMap: {},
      // key -> rule config
      // 模拟天气数据 (因为没有真实API)
      weather: {
        temperature: "24",
        weather: "多云",
        humidity: "65",
        windPower: "2"
      },
      sensorList: [],
      aiAdvice: [
        { type: "info", text: "正在分析环境数据..." }
      ]
    };
  },
  computed: {
    gardenImage() {
      return this.garden.image_path ? this.$baseUrl + this.garden.image_path : "/static/garden_bg.png";
    },
    gardenStatusText() {
      const status = this.garden.status || "normal";
      return status === "normal" ? "正常运行" : "需关注";
    },
    gardenStatusClass() {
      const status = this.garden.status || "normal";
      return status === "normal" ? "tag-primary" : "tag-warn";
    }
  },
  onLoad(options) {
    if (options.garden_id) {
      this.gardenId = options.garden_id;
      this.loadData();
    }
  },
  onPullDownRefresh() {
    this.loadData().then(() => {
      common_vendor.index.stopPullDownRefresh();
    });
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        await this.fetchRules();
        const [garden, devices] = await Promise.all([
          api_garden.getGardenDetail(this.gardenId),
          api_garden.getGardenDevices(this.gardenId)
        ]);
        this.garden = garden;
        this.devices = devices;
        common_vendor.index.setNavigationBarTitle({ title: garden.name });
        await this.fetchSensorData(devices);
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/plot/index.vue:207", e);
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      } finally {
        this.loading = false;
      }
    },
    async fetchRules() {
      try {
        const res = await api_rule.getSensorRules();
        if (res) {
          res.forEach((r) => {
            try {
              this.rulesMap[r.sensor_key] = JSON.parse(r.rule_config);
            } catch (e) {
            }
          });
        }
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/plot/index.vue:225", "Fetch rules failed", e);
      }
    },
    computeStatus(key, value) {
      const num = parseFloat(value);
      if (isNaN(num))
        return null;
      const config = this.rulesMap[key];
      if (!config)
        return null;
      for (const rule of config) {
        const min = rule.min !== null && rule.min !== void 0 ? rule.min : -Infinity;
        const max = rule.max !== null && rule.max !== void 0 ? rule.max : Infinity;
        if (num >= min && num < max) {
          return { label: rule.label, color: rule.color };
        }
      }
      return null;
    },
    async fetchSensorData(devices) {
      const allSensors = [];
      const promises = devices.map(async (device) => {
        try {
          const telemetry = await api_device.getLatestTelemetry(device.id);
          let config = {};
          try {
            if (device.sensor_config) {
              config = JSON.parse(device.sensor_config);
            }
          } catch (e) {
          }
          const latestData = {};
          if (Array.isArray(telemetry)) {
            telemetry.forEach((item) => {
              if (!latestData[item.key])
                latestData[item.key] = item.value;
            });
          } else if (typeof telemetry === "object") {
            Object.assign(latestData, telemetry);
          }
          for (const [key, value] of Object.entries(latestData)) {
            if (config.__ignored && config.__ignored.includes(key))
              continue;
            if (key === "ts")
              continue;
            if (["battery", "signal", "version"].includes(key))
              continue;
            const sensorConf = config[key] || {};
            const name = sensorConf.name || this.formatKeyName(key);
            const unit = sensorConf.unit || this.guessUnit(key);
            const statusObj = this.computeStatus(key, value);
            allSensors.push({
              label: name,
              value: value + unit,
              rawVal: parseFloat(value),
              // 用于AI分析
              key,
              deviceName: device.name,
              status: statusObj ? statusObj.label : null,
              statusColor: statusObj ? statusObj.color : null
            });
          }
        } catch (e) {
          common_vendor.index.__f__("error", "at pages/plot/index.vue:295", `Device ${device.id} telemetry error`, e);
        }
      });
      await Promise.all(promises);
      this.sensorList = allSensors;
      this.lastUpdated = (/* @__PURE__ */ new Date()).toLocaleTimeString();
      this.generateAiAdvice(allSensors);
    },
    formatKeyName(key) {
      const map = {
        "temperature": "温度",
        "humidity": "湿度",
        "soil_moisture": "土壤湿度",
        "light": "光照",
        "co2": "CO2浓度"
      };
      return map[key] || key;
    },
    guessUnit(key) {
      if (key.includes("temp"))
        return "℃";
      if (key.includes("humidity") || key.includes("moisture"))
        return "%";
      if (key.includes("light"))
        return "Lux";
      return "";
    },
    generateAiAdvice(sensors) {
      const advice = [];
      const temp = sensors.find((s) => s.key.includes("temp"));
      sensors.find((s) => s.key.includes("humidity"));
      const soil = sensors.find((s) => s.key.includes("soil"));
      if (temp) {
        if (temp.rawVal > 30)
          advice.push({ type: "warning", text: `气温较高(${temp.value})，注意茶树防晒。` });
        else if (temp.rawVal < 5)
          advice.push({ type: "warning", text: `气温较低(${temp.value})，注意防冻。` });
      }
      if (soil) {
        if (soil.rawVal < 30)
          advice.push({ type: "warning", text: `土壤较干(${soil.value})，建议灌溉。` });
      }
      if (advice.length === 0) {
        advice.push({ type: "info", text: "当前环境适宜，茶树生长状况良好。" });
        advice.push({ type: "info", text: "建议进行常规巡园检查。" });
      }
      this.aiAdvice = advice;
    },
    goEdit() {
      common_vendor.index.navigateTo({ url: `/pages/plot/edit_garden?id=${this.gardenId}` });
    },
    deviceStatusText(status) {
      return status === "online" ? "在线" : "离线";
    },
    deviceStatusClass(status) {
      return status === "online" ? "text-primary" : "text-sub";
    },
    formatTime(time) {
      if (!time)
        return "-";
      return new Date(time).toLocaleString();
    },
    goDeviceDetail(id) {
      common_vendor.index.showToast({ title: "设备详情开发中", icon: "none" });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.garden.name
  }, $data.garden.name ? common_vendor.e({
    b: $options.gardenImage,
    c: common_vendor.t($data.garden.name),
    d: common_vendor.t($options.gardenStatusText),
    e: common_vendor.n($options.gardenStatusClass),
    f: common_vendor.o((...args) => $options.goEdit && $options.goEdit(...args)),
    g: common_vendor.t($data.garden.company || "未归属公司"),
    h: $data.garden.manager
  }, $data.garden.manager ? {
    i: common_vendor.t($data.garden.manager)
  } : {}) : {}, {
    j: common_vendor.t($data.garden.address || "地址未配置"),
    k: common_vendor.t($data.weather.temperature),
    l: common_vendor.t($data.weather.weather),
    m: common_vendor.t($data.weather.humidity),
    n: common_vendor.t($data.weather.windPower),
    o: $data.lastUpdated
  }, $data.lastUpdated ? {
    p: common_vendor.t($data.lastUpdated)
  } : {}, {
    q: $data.sensorList.length > 0
  }, $data.sensorList.length > 0 ? {
    r: common_vendor.f($data.sensorList, (item, index, i0) => {
      return {
        a: common_vendor.t(item.status || "监测中"),
        b: item.statusColor || "#333",
        c: common_vendor.t(item.label),
        d: common_vendor.t(item.value),
        e: index
      };
    })
  } : {}, {
    s: common_vendor.f($data.aiAdvice, (item, index, i0) => {
      return {
        a: common_vendor.t(item.type === "warning" ? "⚠️" : "💡"),
        b: common_vendor.t(item.text),
        c: index,
        d: common_vendor.n(item.type)
      };
    }),
    t: common_vendor.t($data.devices.length),
    v: common_vendor.f($data.devices, (device, k0, i0) => {
      return {
        a: common_vendor.t(device.name),
        b: common_vendor.t($options.deviceStatusText(device.status)),
        c: common_vendor.n($options.deviceStatusClass(device.status)),
        d: common_vendor.t($options.formatTime(device.last_time)),
        e: common_vendor.t(device.sn),
        f: device.id,
        g: common_vendor.o(($event) => $options.goDeviceDetail(device.id), device.id)
      };
    }),
    w: $data.devices.length === 0 && !$data.loading
  }, $data.devices.length === 0 && !$data.loading ? {
    x: common_assets._imports_0
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-a172cb64"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/plot/index.js.map
