"use strict";
const common_http = require("../common/http.js");
function askChatbot(data) {
  return common_http.api.post("/chat/ask", data);
}
function getLatestChat() {
  return common_http.api.get("/chat/latest");
}
exports.askChatbot = askChatbot;
exports.getLatestChat = getLatestChat;
//# sourceMappingURL=../../.sourcemap/mp-weixin/api/chat.js.map
