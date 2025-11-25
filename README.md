# Digital Tea Garden

全栈示例，包含 FastAPI 后端 + uni-app（Vue3）前端 + ML 占位符，支持微信小程序与 H5 演示。

## 目录结构
- `backend/` FastAPI API 服务
  - `app/main.py` 入口，挂载各路由
  - `app/routers/` 业务接口：plots、sensor、advice、disease、chat、stats
  - `app/services/` 规则/模型占位：`rule_engine.py`、`disease_model.py`、`llm_client.py` 等
  - `app/models.py` SQLAlchemy ORM 模型
  - `app/database.py` 数据库连接（支持 MySQL/SQLite）
  - `app/config.py` 配置 & `.env` 读取
  - `requirements.txt` Python 依赖
- `frontend-uni/` uni-app 工程（Vue3）
  - `pages/index/index.vue` 总览页
  - `pages/plot/detail.vue` 地块详情（传感器+今日建议）
  - `pages/disease/disease.vue` 病虫害上传诊断
  - `pages/chat/chat.vue` AI 顾问占位
  - `pages/stats/stats.vue` 统计占位
  - `common/http.js` API 封装，`BASE_URL` 指向后端
- `ml/` 训练占位脚本与数据目录
- `docs/` 草稿文档（API、DB、计划）
- `uploads/` 上传文件目录（默认本地）
- `data/` SQLite 数据文件（默认）

## 技术栈与版本
- 后端：Python 3.9+，FastAPI ≥0.110，SQLAlchemy ≥1.4，Pydantic 1.10.x（<2），uvicorn，python-multipart，PyMySQL
- 前端：uni-app（Vue3 模板，HBuilderX 3.8+），适配微信小程序 + H5
- 数据库：开发默认 SQLite，生产可配 MySQL/MariaDB

## 后端配置与运行
1) 创建并激活环境（conda 或 venv 均可）
```bash
cd backend
python -m venv .venv          # 如用 venv
.\.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

2) 配置数据库与上传目录（可选）  
在 `backend/.env` 写入：
```
# MySQL 示例
DB_URL=mysql+pymysql://user:password@localhost:3306/tea
# 上传目录可自定义
UPLOAD_DIR=../uploads
```
不设 `DB_URL` 时自动使用 SQLite：`../data/tea.db`。

3) 创建数据库表（MySQL 需先手动建库 `CREATE DATABASE tea;`）
```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

4) 运行开发服务
```bash
uvicorn app.main:app --reload --port 8000
```
Swagger: `http://localhost:8000/docs`

## 前端运行（HBuilderX）
1) 打开 `frontend-uni` 目录（Vue3 模板）。  
2) 在 `common/http.js` 设置后端地址：`BASE_URL = 'http://localhost:8000'`（或你的服务器地址）。  
3) 使用 HBuilderX 运行到「浏览器(H5)」或「微信小程序」；如运行小程序需配置 AppID。  

## 常见问题
- Pydantic v2 报错：依赖已锁定 `<2`，请重新安装 `pip install -r requirements.txt`。
- MySQL 连接报错 `Unknown database`: 先在 MySQL 创建对应数据库，再 `create_all`。
- 上传目录不存在：运行时会自动创建 `uploads/`，也可手动创建并在 `.env` 指定路径。

## 后续扩展
- 将 mock 数据替换为真实 CRUD（在各 router 中注入 `Depends(get_db)`）。
- 接入真实病虫害模型和 LLM/ASR 服务（替换 `disease_model.py`、`llm_client.py` 等）。  
- 前端统计页接入 eCharts，增加风险地图与历史报表。  
