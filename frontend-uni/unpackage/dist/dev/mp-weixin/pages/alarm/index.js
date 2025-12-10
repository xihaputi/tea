"use strict";
const common_vendor = require("../../common/vendor.js");
const api_alarm = require("../../api/alarm.js");
const api_task = require("../../api/task.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      activeModule: "alarm",
      // 'alarm' or 'task'
      // Alarm Data
      alarmTabs: ["未读", "已处理", "全部"],
      currentAlarmTab: 0,
      alarms: [],
      // Task Data
      tasks: [],
      // Pagination
      page: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      hasMore: true,
      isRefreshing: false
    };
  },
  onLoad() {
    this.loadData();
  },
  onPullDownRefresh() {
    this.isRefreshing = true;
    this.page = 1;
    this.hasMore = true;
    this.loadData();
  },
  onReachBottom() {
    if (this.hasMore && !this.loading) {
      this.page++;
      this.loadData();
    }
  },
  watch: {
    activeModule() {
      this.resetPagination();
      this.loadData();
    },
    currentAlarmTab() {
      if (this.activeModule === "alarm") {
        this.resetPagination();
        this.loadData();
      }
    }
  },
  methods: {
    switchModule(mod) {
      this.activeModule = mod;
    },
    resetPagination() {
      this.page = 1;
      this.hasMore = true;
      this.alarms = [];
      this.tasks = [];
    },
    async loadData() {
      if (this.loading)
        return;
      this.loading = true;
      try {
        if (this.activeModule === "alarm") {
          await this.loadAlarms();
        } else {
          await this.loadTasks();
        }
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/alarm/index.vue:195", e);
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      } finally {
        this.loading = false;
        if (this.isRefreshing) {
          this.isRefreshing = false;
          common_vendor.index.stopPullDownRefresh();
        }
      }
    },
    async loadAlarms() {
      let status = "";
      if (this.currentAlarmTab === 0)
        status = "active";
      else if (this.currentAlarmTab === 1)
        status = "cleared";
      const res = await api_alarm.getAlarmList({
        page: this.page,
        size: this.pageSize,
        status
      });
      const list = res.list || [];
      if (this.page === 1)
        this.alarms = list;
      else
        this.alarms = [...this.alarms, ...list];
      this.total = res.total || 0;
      this.hasMore = this.alarms.length < this.total;
    },
    async loadTasks() {
      const res = await api_task.getTaskList({
        page: this.page,
        size: this.pageSize,
        status: "pending"
        // Default load pending tasks? Or all? Let's load all for now or handled by backend default
      });
      const list = res.list || [];
      if (this.page === 1)
        this.tasks = list;
      else
        this.tasks = [...this.tasks, ...list];
      this.total = res.total || 0;
      this.hasMore = this.tasks.length < this.total;
    },
    // Alarm Helpers
    severityClass(severity) {
      if (severity === "critical")
        return "bg-critical";
      if (severity === "warning")
        return "bg-warning";
      return "bg-info";
    },
    statusTagClass(status) {
      if (status === "active")
        return "tag-danger";
      return "tag-primary";
    },
    statusText(status) {
      return status === "active" ? "待处理" : "已恢复";
    },
    handleAlarm(item) {
      if (item.status !== "active")
        return;
      common_vendor.index.showActionSheet({
        itemList: ["标记为已处理"],
        success: async (res) => {
          if (res.tapIndex === 0) {
            try {
              await api_alarm.acknowledgeAlarm(item.id);
              common_vendor.index.showToast({ title: "已标志处理", icon: "success" });
              this.resetPagination();
              this.loadData();
            } catch (e) {
              common_vendor.index.showToast({ title: "操作失败", icon: "none" });
            }
          }
        }
      });
    },
    // Task Helpers
    priorityText(p) {
      const map = { high: "高", medium: "中", low: "低" };
      return map[p] || "普通";
    },
    formatDate(d) {
      if (!d)
        return "";
      return new Date(d).toLocaleDateString();
    },
    async completeTask(item) {
      if (item.status === "completed")
        return;
      common_vendor.index.showModal({
        title: "确认",
        content: "确定标记该任务为已完成吗？",
        success: async (res) => {
          if (res.confirm) {
            try {
              await api_task.updateTask(item.id, { status: "completed" });
              common_vendor.index.showToast({ title: "任务已完成" });
              this.resetPagination();
              this.loadData();
            } catch (e) {
              common_vendor.index.showToast({ title: "操作失败", icon: "none" });
            }
          }
        }
      });
    },
    handleTask(item) {
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.activeModule === "alarm" ? 1 : "",
    b: common_vendor.o(($event) => $options.switchModule("alarm")),
    c: $data.activeModule === "task" ? 1 : "",
    d: common_vendor.o(($event) => $options.switchModule("task")),
    e: $data.activeModule === "alarm"
  }, $data.activeModule === "alarm" ? {
    f: common_vendor.f($data.alarmTabs, (t, i, i0) => {
      return {
        a: common_vendor.t(t),
        b: i,
        c: $data.currentAlarmTab === i ? 1 : "",
        d: common_vendor.o(($event) => $data.currentAlarmTab = i, i)
      };
    })
  } : {}, {
    g: $data.activeModule === "alarm"
  }, $data.activeModule === "alarm" ? common_vendor.e({
    h: common_vendor.f($data.alarms, (item, k0, i0) => {
      return {
        a: common_vendor.t(item.gardenName || "未知茶园"),
        b: common_vendor.t(item.deviceName || "未知设备"),
        c: common_vendor.t(item.created_at),
        d: common_vendor.n($options.severityClass(item.severity)),
        e: common_vendor.t(item.content),
        f: common_vendor.t($options.statusText(item.status)),
        g: common_vendor.n($options.statusTagClass(item.status)),
        h: common_vendor.o(($event) => $options.handleAlarm(item), item.id),
        i: item.id
      };
    }),
    i: $data.loading
  }, $data.loading ? {} : {}, {
    j: !$data.loading && $data.alarms.length === 0
  }, !$data.loading && $data.alarms.length === 0 ? {
    k: common_assets._imports_0
  } : {}) : {}, {
    l: $data.activeModule === "task"
  }, $data.activeModule === "task" ? common_vendor.e({
    m: common_vendor.f($data.tasks, (item, k0, i0) => {
      return {
        a: common_vendor.t(item.name),
        b: common_vendor.t($options.priorityText(item.priority)),
        c: common_vendor.n("p-" + (item.priority || "medium")),
        d: common_vendor.t(item.description || "暂无描述"),
        e: common_vendor.t($options.formatDate(item.deadline) || "无截止日期"),
        f: common_vendor.t(item.assignee || "未分配"),
        g: common_vendor.t(item.status === "completed" ? "已完成" : "进行中"),
        h: common_vendor.n(item.status),
        i: common_vendor.t(item.status === "completed" ? "已归档" : "标记完成"),
        j: common_vendor.o(($event) => $options.completeTask(item), item.id),
        k: item.id,
        l: common_vendor.o(($event) => $options.handleTask(item), item.id)
      };
    }),
    n: $data.loading
  }, $data.loading ? {} : {}, {
    o: !$data.loading && $data.tasks.length === 0
  }, !$data.loading && $data.tasks.length === 0 ? {
    p: common_assets._imports_0
  } : {}) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-740bffd5"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/alarm/index.js.map
