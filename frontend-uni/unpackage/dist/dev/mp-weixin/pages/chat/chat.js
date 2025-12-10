"use strict";
const common_vendor = require("../../common/vendor.js");
const api_chat = require("../../api/chat.js");
const _sfc_main = {
  data() {
    return {
      question: "",
      history: [],
      sessionId: null,
      loading: false
    };
  },
  onLoad() {
    this.loadHistory();
  },
  methods: {
    async loadHistory() {
      try {
        const res = await api_chat.getLatestChat();
        if (res.session_id) {
          this.sessionId = res.session_id;
          this.history = res.history || [];
          this.scrollToBottom();
        }
      } catch (e) {
        common_vendor.index.__f__("error", "at pages/chat/chat.vue:70", "Failed to load history", e);
      }
    },
    async ask() {
      if (!this.question || this.loading)
        return;
      const content = this.question;
      this.question = "";
      this.history.push({ role: "user", content });
      this.scrollToBottom();
      this.loading = true;
      try {
        const res = await api_chat.askChatbot({
          question: content,
          history: this.history.map((m) => ({ role: m.role, content: m.content })),
          session_id: this.sessionId
        });
        if (res.session_id) {
          this.sessionId = res.session_id;
        }
        this.history.push({ role: "assistant", content: res.answer });
      } catch (e) {
        this.history.push({ role: "assistant", content: "抱歉，我现在无法回答，请稍后再试。" });
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      setTimeout(() => {
        common_vendor.index.pageScrollTo({ scrollTop: 99999, duration: 300 });
      }, 100);
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.f($data.history, (msg, idx, i0) => {
      return common_vendor.e({
        a: msg.role === "assistant"
      }, msg.role === "assistant" ? {} : {}, {
        b: common_vendor.t(msg.content),
        c: common_vendor.n(msg.role === "user" ? "bubble-user" : "bubble-ai"),
        d: msg.role === "user"
      }, msg.role === "user" ? {} : {}, {
        e: idx,
        f: common_vendor.n(msg.role === "user" ? "msg-right" : "msg-left")
      });
    }),
    b: $data.loading
  }, $data.loading ? {} : {}, {
    c: common_vendor.o((...args) => $options.ask && $options.ask(...args)),
    d: $data.question,
    e: common_vendor.o(($event) => $data.question = $event.detail.value),
    f: common_vendor.o((...args) => $options.ask && $options.ask(...args)),
    g: !$data.question || $data.loading ? 1 : ""
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-0a633310"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/chat/chat.js.map
