# 2026-06-12 Demo 项目开发进度记录

## 一、文档依据

本次进度整理基于以下两份项目规划文档：

- `/mnt/d/ZephyrNote/学习笔记/g2-service项目学习/demo项目最大效益学习流程/最终展示字段说明及后端返回结构.md`
- `/mnt/d/ZephyrNote/学习笔记/g2-service项目学习/demo项目最大效益学习流程/demo项目最大效益学习流程.md`

本次整理同时结合了今天的前后端实际开发结果。

## 二、今日完成内容

### 1. 前端展示链已完成第一阶段

- 已完成前端静态展示页面。
- 已完成访客风险面板主视图，包括：
  - `visitor_id`
  - `risk_level`
  - `risk_code`
  - `risk_summary`
  - 访问摘要区
  - 技术信号区
  - 原始风控摘要区
- 已支持 `pass / review / reject` 三种场景切换。
- 已完成浏览器基础信号采集工具，当前可采集并组织以下字段：
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
  - `user_agent`
  - `canvas_fingerprint`
  - `webgl_vendor`
  - `webgl_renderer`

### 2. 后端统一接口已完成第一版

- 已创建独立 FastAPI Demo 后端。
- 已完成基础应用入口与路由注册。
- 已完成：
  - `GET /api/health`
  - `GET /api/visitor`
  - `POST /api/visitor`
- 已接入 CORS，允许前端本地开发地址访问。

### 3. 前后端契约已基本对齐

- 已按照规划文档中的目标结构建立统一返回 DTO。
- 已完成 Pydantic 响应模型：
  - `VisitorResponse`
  - `Network`
  - `Environment`
  - `Signals`
  - `Meta`
- 已完成请求模型：
  - `VisitorRequest`
  - `VisitorEnvironmentInput`
  - `VisitorSignalsInput`
- 已抽出 `ScenarioType`，统一 `pass / review / reject` 的类型约束。

### 4. 后端已具备接收前端信号并回填响应的能力

- 当前 `POST /api/visitor` 已可接收前端上传的 `environment` 与 `signals`。
- 后端当前会基于 mock 场景做深拷贝，并将前端上传字段覆盖到响应结果中。
- 已形成初步 service 分层：
  - 路由层负责 HTTP 接口
  - service 层负责 profile 获取与字段合并
  - data 层负责 mock 数据
  - schema 层负责请求与响应结构

### 5. 阶段性成果已归档到 GitHub

- 后端阶段性提交已完成并推送。[zljcode/Back-end: 获取指纹，评估风险后端服务](https://github.com/zljcode/Back-end)
- 前端阶段性提交已完成并推送。[zljcode/Front-end: 获取指纹，评估风险前端服务](https://github.com/zljcode/Front-end)

## 三、当前项目所处阶段

结合原始规划文档，当前项目大致处于以下位置：

### 已完成

- 第 2 阶段：小 Python 后端第一版
- 第 3 阶段：前端页面第一版
- 前后端稳定 DTO 基本建立
- 前端开始向后端发送浏览器基础信号

### 部分完成

- 前后端联调链路已具备代码基础，但仍需要完整跑通与验证
- 浏览器信号采集已开始，但仍属于基础版本

### 尚未开始或尚未完成

- 第 4 阶段：真实 `risk_query` 接入
- 第 6 阶段：匿名模式启发式判断
- 第 6 阶段：VPN / 代理判断
- 第 7 阶段：完整 `client_report -> token_query`

## 四、当前可确认的能力边界

### 已具备的能力

- 页面可以展示完整 Demo 结构
- 后端可以稳定返回符合展示契约的数据
- 前端可以将基础浏览器环境信息发送给后端
- 后端可以用前端上传的环境字段覆盖 mock 返回结果

### 当前仍是 mock 的部分

- `risk_level`
- `risk_code`
- `risk_summary`
- `is_incognito`
- `incognito_confidence`
- `is_vpn`
- `vpn_confidence`
- `ip_type`
- `visitor_id`

### 当前尚未进入真实业务判断的部分

- 风险码来源仍非真实风控接口
- 后端尚未接入 `sign_token` 生成
- 后端尚未调用真实 `risk_query`
- 前端尚未做匿名模式启发式检测
- 后端尚未做基于风控结果的 VPN/代理映射

## 五、当前存在的剩余问题

### 1. 前后端联调还需要做一次完整验证

- 后端服务启动方式需要统一使用 `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- 需要验证 `POST /api/visitor` 在页面刷新、场景切换、错误情况下的表现

### 2. 前端 `visitorService` 仍需要进一步收口

- 当前数据流已经指向后端接口
- 但错误处理与是否保留本地 fallback 仍需要做最终决策
- `API_BASE_URL` 当前是直接写死，后续应整理成可配置项

### 3. 真实风控链路尚未接入

- 尚未读取 `app_id`
- 尚未读取 `private_key`
- 尚未生成 `gen_time`
- 尚未生成 `sign_token`
- 尚未调用真实 `risk_query`
- 尚未将真实风控结果映射到 Demo DTO

### 4. 浏览器信号仍属于基础版

- 当前重点仍是基础环境字段
- `canvas_fingerprint`、`webgl_vendor`、`webgl_renderer` 已有字段位，但还没有更深入处理
- 尚未补充匿名模式检测相关信号
- 尚未补充更接近真实风控链路所需的指纹上下文

## 六、后续剩余开发计划

建议仍然按照原始规划文档的顺序推进，避免过早进入完整复杂链路。

### 第一优先级：跑通前后端联调

1. 启动后端 FastAPI 服务
2. 启动前端静态服务
3. 验证页面实际请求 `POST /api/visitor`
4. 验证前端上传信号能够真实体现在后端返回结果中
5. 修正联调过程中暴露的请求字段、响应字段和错误处理问题

### 第二优先级：收紧当前 Demo 第一版

1. 统一前端错误处理策略
2. 统一前端配置项管理
3. 补一次后端运行说明与启动说明
4. 补最小联调验证记录

### 第三优先级：进入真实 `risk_query`

1. 梳理 `risk_query` 调用所需参数
2. 完成 `sign_token` 生成逻辑
3. 在后端接入真实 `risk_query`
4. 将真实 `risk_level` 和 `risk_code` 映射到当前响应结构
5. 保持前端页面结构不变，只替换数据来源

### 第四优先级：增强浏览器信号与状态判断

1. 补匿名模式启发式检测
2. 补更完整的浏览器端信号采集
3. 结合真实风控结果处理 VPN / 代理状态
4. 完善 `incognito_confidence`、`vpn_confidence` 三态表达

### 第五优先级：挑战完整真实链路

1. 回头补读 `g2-service` 核心调用链
2. 研究 `client_report`
3. 研究 `token_query`
4. 尝试完整 `client_report -> token_query`

## 七、当前结论

截至 `2026-06-12`，本项目已经完成从“纯前端 mock 展示”到“具备后端接口、统一 DTO、可接收浏览器基础信号”的阶段性推进。

当前最合理的下一步不是直接进入完整风控主链路，而是先把前后端联调跑通，再在这个稳定壳子上逐步替换成真实 `risk_query` 和更完整的浏览器指纹能力。

