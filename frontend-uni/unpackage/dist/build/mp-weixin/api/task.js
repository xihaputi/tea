"use strict";const t=require("../common/http.js");exports.getTaskList=function(s){return t.api.get("/tasks/",s)},exports.updateTask=function(s,e){return t.api.put(`/tasks/${s}`,e)};
