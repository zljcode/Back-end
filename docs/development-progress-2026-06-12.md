# Demo 项目统一开发进度记录

## 文档说明

这份文档用于统一记录 Demo 项目的前后端开发进度。

整理依据包括：

- `/mnt/d/ZephyrNote/学习笔记/g2-service项目学习/demo项目最大效益学习流程/最终展示字段说明及后端返回结构.md`
- `/mnt/d/ZephyrNote/学习笔记/g2-service项目学习/demo项目最大效益学习流程/demo项目最大效益学习流程.md`
- `/demo/Front-end/docs/development-progress.md`

当前文档已经吸收前端阶段记录，并结合后端当前实际代码状态进行合并更新。

## 2026-06-12 第一阶段：前端 Demo 第一版

### 本阶段目标

先完成一个可运行、可展示的浏览器访客风险面板，用 mock 数据跑通展示链路，后续再逐步接入 Python 后端与真实风控接口。

### 已完成内容

- 创建静态前端项目结构。
- 新增页面入口：
  - `index.html`
  - `src/main.js`
- 新增主视图组件：
  - `src/components/visitorDashboard.js`
- 新增 mock 数据：
  - `src/data/mockVisitor.js`
- 新增前端数据服务层：
  - `src/services/visitorService.js`
- 新增浏览器信号采集工具：
  - `src/utils/browserSignals.js`
- 新增主样式与基础工具函数。

### 当前页面能力

- 展示 `visitor_id`
- 展示 `risk_level`
- 展示 `risk_code`
- 展示 `risk_summary`
- 展示访问摘要：
  - IP
  - 浏览器名称与版本
  - 操作系统
  - 设备类型
  - 匿名模式状态
  - VPN / 代理状态
- 展示技术信号：
  - `user_agent`
  - `language`
  - `timezone`
  - `platform`
  - `screen_resolution`
  - `hardware_concurrency`
  - `device_memory`
  - `webgl_vendor`
  - `webgl_renderer`

## 2026-06-12 第二阶段：后端接口第一版

### 本阶段目标

建立一个独立的 FastAPI Demo 后端，统一前端展示所需返回结构，先用 mock 数据打通后端接口层。

### 已完成内容

- 创建独立 FastAPI 后端项目。
- 完成基础应用入口与路由注册。
- 完成接口：
  - `GET /api/health`
  - `GET /api/visitor`
  - `POST /api/visitor`
- 接入 CORS，允许本地前端开发地址访问。
- 建立统一返回 DTO：
  - `VisitorResponse`
  - `Network`
  - `Environment`
  - `Signals`
  - `Meta`
- 建立统一请求 DTO：
  - `VisitorRequest`
  - `VisitorEnvironmentInput`
  - `VisitorSignalsInput`
- 抽出 `ScenarioType`，统一 `pass / review / reject` 约束。

## 2026-06-15 第三阶段：前后端联调

### 本阶段完成内容

- 前端主数据链已从本地 mock 主流程切换为请求后端 `/api/visitor`。
- 浏览器环境信号会通过 `POST /api/visitor` 发送给后端。
- 后端会返回与前端页面 DTO 对齐的结构，前端展示层无需推翻重写。
- 前后端联调环境下，本地页面可正确请求本地后端。

### 浏览器信号链路

当前前端已能采集并上传以下 `environment` 字段：

- `browser_name`
- `browser_version`
- `os_name`
- `device_type`
- `language`
- `timezone`
- `platform`
- `screen_resolution`
- `hardware_concurrency`
- `device_memory`

当前前端已能采集并上传以下 `signals` 字段：

- `user_agent`
- `canvas_fingerprint`
- `webgl_vendor`
- `webgl_renderer`

### 当前后端处理方式

- `GET /api/visitor`
  - 仍保留场景 mock，用于 `pass / review / reject` 展示。
- `POST /api/visitor`
  - `visitor_id / risk_level / risk_code / risk_summary / network` 仍来自后端场景数据或占位逻辑。
  - `environment / signals` 已切换为以前端实报为主构造返回结果。
  - `meta.request_time` 由后端动态生成。

## 2026-06-15 第四阶段：匿名模式与技术信号增强

### 已完成内容

- 已为前端接入匿名模式启发式检测逻辑。
- 前端会将 `is_incognito` 和 `incognito_confidence` 上报后端。
- 后端会将匿名模式相关字段返回给前端页面。
- 页面摘要区已开始展示真实匿名模式检测结果，而不是固定 mock 值。
- `Canvas Fingerprint`、`WebGL Vendor`、`WebGL Renderer` 已进入真实采集链路。

### 当前展示语义

- `Likely Incognito`：检测到较强匿名模式信号。
- `Not Detected`：当前规则没有命中明显匿名模式特征。
- `Unknown`：当前环境没有足够强的匿名模式证据。

## 2026-06-15 第五阶段：VPN 检测后端能力预留

### 已完成内容

- 后端已在路由层接入 `Request`。
- 已实现客户端 IP 提取逻辑：
  - 优先读取 `X-Forwarded-For`
  - 其次读取 `X-Real-IP`
  - 最后回退到 `request.client.host`
- 后端 `POST /api/visitor` 已能将 `client_ip` 写入 `network.ip`。
- 已预留 `_detect_vpn(client_ip)` 函数。
- 当前已完成基础保底判断：
  - `127.0.0.1`
  - `::1`
  - 私网 IP
  - 保留地址
  - 非法 IP 字符串
  以上情况统一返回 `unknown`

### 当前结论

- VPN / 代理识别本质上依赖外部 IP intelligence、风控结果或公网 IP 情报库。
- 当前项目已完成“后端检测入口与返回结构预留”，但尚未具备真实 VPN 识别能力。
- 当前阶段不会继续手写复杂 VPN 判断规则，后续应通过外部能力或 `risk_query` 结果接入。

## 当前整体状态

### 已完成

- 前端页面第一版完成
- 后端 FastAPI 第一版完成
- 前后端 DTO 基本建立
- 前后端联调已打通
- 浏览器基础信号已从前端上传到后端
- `environment / signals` 已改为以前端实报为主
- 匿名模式启发式检测已接入
- VPN 检测后端入口已预留

### 当前仍为 mock 或占位的部分

- `visitor_id`
- `risk_level`
- `risk_code`
- `risk_summary`
- `network.ip_type`
- `network.is_vpn`
- `network.vpn_confidence`

### 当前尚未进入真实业务判断的部分

- 真实 `risk_query`
- `sign_token` 生成
- `app_id / private_key` 配置接入
- 基于真实风控结果的 VPN / 代理映射
- 完整 `client_report -> token_query`

## 当前能力边界

### 已具备的能力

- 页面可展示完整 Demo 结构
- 页面可展示真实浏览器环境字段
- 后端可接收并返回前端实报的浏览器环境与信号
- 后端可提取请求来源 IP
- 本地联调环境下可在 `network.ip` 中展示真实请求来源地址

### 当前限制

- 本地联调时，`network.ip` 显示 `127.0.0.1` 或 `::1` 属于正常现象，不代表公网真实 IP。
- VPN 判断当前只能停留在 `unknown` 三态兜底。
- 风险结果仍然不是权威风控输出。

## 后续开发计划

### 第一优先级：收紧当前联调版本

1. 再做一次前后端联调回归验证。
2. 检查页面展示值是否全部来自后端返回，而非前端残留兜底。
3. 收一下前端 `visitorService` 的错误处理与配置项管理。

### 第二优先级：接入真实 `risk_query`

1. 梳理 `risk_query` 请求参数。
2. 接入 `app_id`、`private_key`。
3. 完成 `sign_token` 生成。
4. 调用真实 `risk_query`。
5. 将真实 `risk_level / risk_code` 映射到当前 DTO。

### 第三优先级：增强状态判断

1. 完善匿名模式检测规则。
2. 在接入外部能力或 `risk_query` 后再做 VPN / 代理判断。
3. 继续增强浏览器信号采集，但保持 DTO 稳定。

### 第四优先级：挑战完整业务链路

1. 回头补读 `g2-service` 主链路。
2. 研究 `client_report`
3. 研究 `token_query`
4. 尝试完整 `client_report -> token_query`

## 当前结论

截至 `2026-06-15`，项目已经从“纯前端 mock 页面”推进到“前后端联调完成、浏览器信号可真实上报、匿名模式链路已接入、VPN 检测后端入口已预留”的阶段。

当前最合理的下一步不是继续硬写本地 VPN 识别，而是先把现有联调版本收稳，然后尽快进入真实 `risk_query` 接入阶段。
