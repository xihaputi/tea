"use strict";const t=require("../common/http.js");exports.askChatbot=function(e){return t.api.post("/chat/ask",e)},exports.getLatestChat=function(){return t.api.get("/chat/latest")};
