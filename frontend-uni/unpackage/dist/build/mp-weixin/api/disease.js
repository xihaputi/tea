"use strict";const e=require("../common/http.js");exports.detectDisease=function(t,s){return e.api.upload("/disease/detect",t,"file",{plot_id:s||""})};
