# ST Deck Agent 项目复盘 Playbook

> 面向「把 Skill 做成可分享工具」的参考手册。  
> 基于 ST Deck Agent 从 Skill 文档 → Cloud Run 内部产品的完整实践整理。

---

## 一、项目演进脉络

```
Skill 文档 + 本地脚本
    → python-pptx + st_brand.py 品牌库
    → Copilot/Cursor Skill（SKILL.md 合并）
    → Cloud Run 产品（Cursor SDK + Web UI）
    → 生产加固（鉴权 / TTL / 限流）
    → UI 产品化 + User Guide + GitHub
```

**核心转变：** 从「我会用 AI 做 PPT」→「同事打开 URL 就能用」。

难点不在 Agent 能力，而在 **Serving 层**（会话、安全、稳定性、体验）。

---

## 二、做得好的、可复用的经验

### 2.1 分层设计：Agent 层 vs Serving 层

| 层 | 职责 | 本项目做法 |
|----|------|------------|
| **Agent 层** | 怎么做对 | `SKILL.md` + `AGENTS.md` + `st_brand.py` + preview 自检闭环 |
| **Serving 层** | 怎么稳定地跑 | FastAPI、会话、鉴权、限流、TTL、SSE |
| **体验层** | 怎么让人会用 | Web UI、User Guide、示例 chips、状态 pill |

**经验：** Agent 层打到 8/10 往往够用；Serving 层不到 6/10 就不该广撒 URL。

### 2.2 Skill 不要只停留在 Markdown

| 形态 | 作用 |
|------|------|
| `SKILL.md` | 品牌 / 流程的**规范真理源** |
| `AGENTS.md` | **工作流**（读 SKILL、不重复字号等规则） |
| `st_brand.py` 等代码库 | **可执行约束**（色板、对比度、`closing_slide()`） |
| `tools/preview.py` | **闭环验证**（生成后必须「看见」结果） |

**经验：** 只靠 prompt 复述 SKILL，规则会漂移、会被违反。

**可复制目录结构：**

```
skills/<name>/SKILL.md          ← 规范（单一真理源）
workspace_template/
  AGENTS.md                     ← 流程 + 「详见 SKILL」
  <domain>_helpers.py           ← 品牌/领域代码化
  tools/preview.py              ← 自检
```

### 2.3 双模式产品策略

- **默认一次性（One-shot）**：无人值守、直接出稿 → 适合约 90% 内部场景
- **对话模式标 Beta**：首轮规划（大纲 + 追问），用户确认后再 BUILD；需 `--max-instances 1`、内存态 agent、重启丢上下文 → 文档写清楚，不作为主路径

**经验：** 先 ship 一次性；对话等有外部 session store 再做。

### 2.4 内部工具的「最低生产套餐」

上线前建议齐备：

| 能力 | 说明 |
|------|------|
| `ACCESS_TOKEN` | 共享口令（管理员发放，非申请制 API key） |
| 上传限制 | 单文件 / 总大小 / 文件数上限 |
| 会话 TTL | Cloud Run `/tmp` 在内存上，必须定期清理 |
| `run_in_executor` | `copytree`、GCS 等阻塞 I/O 不堵事件循环 |
| Agent run 超时 | 避免卡死占连接 |
| 错误脱敏 | 内部异常写日志，用户只见友好消息 |
| 依赖 pin | `requirements.txt` 锁版本 |
| 双文档 | `README.md`（部署者）+ User Guide HTML（使用者） |

### 2.5 文档与代码同步交付

- **README.md**：环境变量、gcloud 命令、架构说明
- **User Guide HTML**：口令获取、操作流程、FAQ、中英切换
- 风格对齐团队已有工具（如 Resume Screener）降低认知成本

### 2.6 Git 与仓库 hygiene

- 项目目录**单独** `git init`，勿在用户主目录误 init
- `.gitignore` 排除 `.env`、`*.pptx`、会话输出
- 推 GitHub 后可用 `gcloud run deploy --source .` 从仓库部署

---

## 三、踩过的坑与教训

### 3.1 部署与运维

| 问题 | 原因 | 教训 |
|------|------|------|
| 构建失败 / 空白页 | 在错误目录 deploy；`index.html` 0 字节 | deploy 前 `wc -c` 校验关键文件 |
| 权限错误 | Cloud Shell 上 root 拥有的目录 | 重新上传整个项目文件夹 |
| 上传慢 | 传了整个 home 目录 | 只传 `st-deck-agent` 目录 |
| OOM | `/tmp/sessions` 永不清理 | 必须 TTL + 定期 sweep |
| 冷启动慢 | LibreOffice + Chromium 镜像大 | 接受或设 `min-instances=1` |

### 3.2 Agent 与品牌

| 问题 | 原因 | 教训 |
|------|------|------|
| 白字 on 浅底 | Agent 手搓颜色 | `text_on(fill)` 写进库，prompt 只引用 |
| 规则漂移 | SKILL / AGENTS / runner 三处重复 | **单一真理源**：prompt 写「见 SKILL」 |
| 外发缺 closing | 只有 `footer()` | 合规清单 → 补 `closing_slide()` 构造器 |
| 预览与 PPT 字体差 | Docker 用 Liberation Sans | User Guide 说明，以本机 .pptx 为准 |

### 3.3 前端

| 问题 | 原因 | 教训 |
|------|------|------|
| Agent 进度竖排 | SSE 每 token 一个 `<div>` | 流式合并到同一气泡 |
| 按钮锁死 | 无 try/finally | 所有 handler 统一 `runStream` |
| 误显示「完成」 | 未跟踪 SSE `error` | `hadError` 状态机 |
| 漂亮 UI 缺鉴权 | 两版 HTML 各管一摊 | **以产品 UI 为壳，并入后端能力** |

### 3.4 架构

| 问题 | 教训 |
|------|------|
| 对话模式内存态 | 设计取舍，非 bug；持久对话需外部 store |
| 同步 I/O 堵事件循环 | GCS / copytree 必须 `run_in_executor` |
| 无鉴权 + 无限流 | 内部 URL 一扩散 = 半公开 |
| `sid` 12 位 hex | 不能当安全边界，必须口令或 IAP |

---

## 四、Skill → 可分享项目 Playbook

### Phase 0：Skill 是否适合产品化？

**适合：**

- 输出可文件化（pptx / pdf / png）
- 有明确自检标准（品牌、对比度、页数）
- 同事重复劳动多

**暂缓产品化：**

- 强依赖本地机密数据
- 需要复杂多人协作审批
- 单次运行 >10 分钟且无异步通知

### Phase 1：Skill 固化（约 1–2 天）

1. 合并 `SKILL.md`（单一入口 + `references/`）
2. 写 `AGENTS.md`（模式、循环、产物路径）
3. 抽 `<domain>_helpers.py`（把「必须遵守」写进代码）
4. 写 `tools/preview.py`（可视化自检）
5. 本地 build 脚本跑通 2–3 个真实案例

**交付物：** 本地能稳定产出 + preview PNG。

### Phase 2：最小 Serving（约 3–5 天）

```
st-<tool>-agent/
├── app/
│   ├── main.py          # FastAPI + SSE
│   ├── runner.py        # Cursor SDK 编排
│   ├── config.py        # 环境变量集中
│   ├── security.py      # 口令 + 限流 + 错误脱敏
│   └── sessions.py      # 会话 + TTL + GCS（可选）
├── workspace_template/  # 每次会话 copy 的「脑」
│   ├── AGENTS.md
│   ├── skills/...
│   ├── <helpers>.py
│   └── tools/
├── Dockerfile
├── requirements.txt     # pin 版本
└── README.md
```

**关键决策：**

- Brain = `workspace_template`（随会话复制）
- 产物 = `output/deck.pptx` + `preview-*.png` + `build.py`
- 下载名 = `deck_meta.json` 或从 request 推导

### Phase 3：体验与上线（约 2–3 天）

- Web UI：左输入、右工作台（idle → run → done）
- `ACCESS_TOKEN` + User Guide HTML
- Cloud Run deploy + 口令私下发放
- GitHub 仓库（便于 `--source` 部署）

### Phase 4：加固（按需分批）

| 包 | 内容 |
|----|------|
| **A — 生产底线** | 鉴权、TTL、上传限制、依赖 pin、错误脱敏 |
| **B — 并发稳定** | executor、run 超时、`asyncio.Queue` SSE、`tarfile` filter |
| **C — 品牌产品** | `closing_slide()`、对比度边界、真理源统一、README |

**不要一次全做**；先 A 再广撒 URL。

---

## 五、检查清单

### Skill 层

- [ ] `SKILL.md` 自洽、可单独阅读
- [ ] `references/` 分拆细节
- [ ] 关键规则进入代码库（不仅 prompt）
- [ ] 有 preview / 自检步骤
- [ ] 外发合规有明确构造器（如 closing slide）

### Serving 层

- [ ] `ACCESS_TOKEN` 或 IAP
- [ ] 限流 + 上传限制
- [ ] 会话 TTL
- [ ] 阻塞 I/O 走 executor
- [ ] Agent 超时
- [ ] 错误不泄露内部栈

### 体验层

- [ ] 一次性默认路径 ≤ 3 次点击
- [ ] 进度可读（流式合并）
- [ ] 失败可恢复（按钮不锁死）
- [ ] 下载名有意义（`主题-日期.ext`）
- [ ] User Guide（口令、FAQ、限制）

### 运维层

- [ ] README 含完整 deploy 命令
- [ ] 环境变量表
- [ ] 独立 git 仓库 + `.gitignore`
- [ ] deploy 前校验关键文件非空

---

## 六、核心原则（给下一个项目）

1. **Skill 是规范，代码是约束，preview 是验收。**
2. **Agent 聪明不够，Serving 要当产品做。**
3. **内部工具也要有口令、限流和清理。**
4. **UI 和 backend 能力要合并，不要两套 HTML 各管一半。**
5. **先一次性跑通再搞对话；先 A 包再扩受众。**
6. **文档两类读者：部署者看 README，使用者看 User Guide。**

---

## 七、命名与模板泛化

| 本项目 | 可泛化 |
|--------|--------|
| `st-deck-agent` | `st-<artifact>-agent` |
| `st_brand.py` | `<org>_<domain>_helpers.py` |
| `deck.pptx` | `output/artifact.<ext>` |
| `skills/st-ppt-brand/SKILL.md` | `skills/<skill-name>/SKILL.md` |
| `ACCESS_TOKEN` | 通用内部工具口令模式 |
| `workspace_template/` | 每次会话复制的 Agent 工作区 |

---

## 八、相关资源

| 资源 | 位置 |
|------|------|
| 代码仓库 | https://github.com/Yude-Jiang/st-deck-agent |
| 部署说明 | 仓库根目录 `README.md` |
| 使用者指南 | `docs/ST_Deck_Agent_User_Guide.md` · [HTML](ST_Deck_Agent_User_Guide.html) |
| 品牌 Skill | `workspace_template/skills/st-ppt-brand/SKILL.md` |

---

*ST China AI Force · 2026*
