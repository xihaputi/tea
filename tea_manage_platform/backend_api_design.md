# Tea Manage Platform 后端接口设计文档

根据前端页面需求，整理出以下后端接口列表。

## 1. 认证模块 (Auth)

| 接口名称 | URL | Method | 请求参数 (Body/Query) | 响应数据 (Data) |
| :--- | :--- | :--- | :--- | :--- |
| **用户登录** | `/api/auth/login` | `POST` | `{ username, password }` | `{ token, userInfo }` |
| **获取用户信息** | `/api/auth/user/info` | `GET` | - | `{ id, name, avatar, roles }` |
| **退出登录** | `/api/auth/logout` | `POST` | - | - |

## 2. 仪表盘 (Dashboard)

| 接口名称 | URL | Method | 请求参数 | 响应数据 |
| :--- | :--- | :--- | :--- | :--- |
| **获取统计指标** | `/api/dashboard/stats` | `GET` | - | `{ gardenCount, deviceCount, alertCount, onlineRate }` |

## 3. 茶园管理 (Tea Garden)

### 茶园基础
| 接口名称 | URL | Method | 请求参数 | 响应数据 |
| :--- | :--- | :--- | :--- | :--- |
| **获取茶园列表** | `/api/tea-gardens` | `GET` | `page, size, name, company` | `{ list: [], total }` |
| **新增茶园** | `/api/tea-gardens` | `POST` | `{ name, address, manager, ... }` | `{ id }` |
| **获取茶园详情** | `/api/tea-gardens/{id}` | `GET` | - | `{ id, name, address, area, desc, ... }` |
| **更新茶园信息** | `/api/tea-gardens/{id}` | `PUT` | `{ name, address, area, ... }` | - |
| **删除/停用茶园** | `/api/tea-gardens/{id}` | `DELETE` | - | - |

### 地块与关联
| 接口名称 | URL | Method | 请求参数 | 响应数据 |
| :--- | :--- | :--- | :--- | :--- |
| **获取地块列表** | `/api/tea-gardens/{id}/plots` | `GET` | - | `[{ code, variety, area, devices: [] }]` |
| **新增地块** | `/api/tea-gardens/{id}/plots` | `POST` | `{ code, variety, area }` | `{ id }` |
| **获取关联设备** | `/api/tea-gardens/{id}/devices` | `GET` | - | `[{ id, name, type, status }]` |

## 4. 设备管理 (Device)

| 接口名称 | URL | Method | 请求参数 | 响应数据 |
| :--- | :--- | :--- | :--- | :--- |
| **获取产品分组** | `/api/devices/products` | `GET` | - | `[{ id, label, children: [] }]` |
| **获取设备列表** | `/api/devices` | `GET` | `page, size, keyword, status, productId` | `{ list: [], total }` |
| **注册新设备** | `/api/devices` | `POST` | `{ name, sn, productId }` | `{ id }` |
| **获取设备详情** | `/api/devices/{id}` | `GET` | - | `{ id, name, sn, product, status, lastTime }` |
| **获取最新遥测** | `/api/devices/{id}/telemetry` | `GET` | - | `{ temp, humi, ... }` |
| **获取历史数据** | `/api/devices/{id}/telemetry/history` | `GET` | `startTs, endTs, keys` | `{ [key]: [{ts, value}] }` |

## 5. 规则引擎 (Rule Engine)

| 接口名称 | URL | Method | 请求参数 | 响应数据 |
| :--- | :--- | :--- | :--- | :--- |
| **获取规则列表** | `/api/rules` | `GET` | `page, size` | `{ list: [], total }` |
| **新建规则** | `/api/rules` | `POST` | `{ name, condition, actions: [] }` | `{ id }` |
| **更新规则** | `/api/rules/{id}` | `PUT` | `{ name, condition, actions: [] }` | - |
| **切换启用状态** | `/api/rules/{id}/enable` | `PUT` | `{ enabled: boolean }` | - |
| **删除规则** | `/api/rules/{id}` | `DELETE` | - | - |
