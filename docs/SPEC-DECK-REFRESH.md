# Deck 焕新 — 实施 Spec（Scaffold / 独立分支）

> **分支：** `cursor/deck-refresh-scaffold-cc52`  
> **状态：** Draft PR — 验证通过后再考虑 merge `main`  
> **产品需求：** `docs/PRD-DECK-REFRESH.md`  
> **原则：** 不修改 Deck 生成（`/generate`、`/edit`、`/chat/*`、`runner.py` 生成语义）

---

## 本 PR 范围（Scaffold）

- [x] `config/` 合规配置占位（Purview GUID、关键词 **默认关闭**）
- [x] `app/refresh/` 合规扫描管道骨架（**仅 file integrity 实现**）
- [x] `REFRESH_ENABLED` / `REFRESH_IMPLEMENTED` 环境变量（默认 `false`）
- [x] `/api/config` 暴露焕新开关（前端尚未接 Tab）
- [ ] 规则引擎 `refresh_deck.py` — 后续 PR
- [ ] `/refresh/*` API + UI Tab — 后续 PR

**对现网 Deck 生成的影响：无**（开关默认关闭，无新用户可见功能）

---

## 关键设计决策（实施时必须遵守）

### 1. Agent advise：物理无工具边界

焕新「建议」步骤 **不得** 使用 `LocalAgentOptions` 全功能 agent。  
一次性多模态调用（图 + changelog → Markdown 文本），无 cwd / shell / 写文件。  
失败不阻塞 `deck-refreshed.pptx` 下载。

### 2. 规则引擎：`refresh_deck.py`

确定性 `python-pptx` 脚本，**不依赖 LLM**。  
Autofit 关闭前做溢出预检；装饰形状判定用显式布尔条件；阈值进 `refresh_rules_config.py`。  
`refresh_changelog.json` 为唯一变更真相源。

### 3. 合规扫描（v1 与预留）

| 层 | v1 本分支 | 预留 |
|---|---|---|
| `file_integrity` | **实现** | — |
| `purview_guid` | `skip`（`purview_enabled: false`） | `config/purview_labels.json` |
| `keyword` | `skip`（`keyword_enabled: false`） | `config/compliance_keywords.json` |

**GUID：** v1 不实现；配置与管道接口预留，v1.1+ 可启用。  
**关键词：** 机制预留，词表默认为空；启用时只改 JSON + `compliance.json` 开关。

### 4. 会话与安全

- refresh 会话 **禁止 GCS 备份**（`REFRESH_GCS_BACKUP=false` 默认）
- 会话目录与生成隔离（`mode=refresh` / `refresh-{sid}`）
- `uploads/original.pptx` 永不覆盖
- 结束后主动清理（不依赖 TTL 为主策略）— 完整实现待后续 PR

### 5. 硬约束

- 不改 `/generate`、`/edit`、`/chat/*` 行为
- 不把焕新逻辑放进 `workspace_template/`（可 import `st_brand` **常量**）
- 不删页、不调序、不增页、不追加 closing
- 不改幻灯片文字与数据

---

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `REFRESH_ENABLED` | `false` | 前端/API 是否暴露焕新（merge 后仍默认关） |
| `REFRESH_IMPLEMENTED` | `false` | 端到端焕新是否可用 |
| `MAX_REFRESH_PAGES` | `20` | 焕新页数上限 |
| `REFRESH_GCS_BACKUP` | `false` | refresh 会话是否允许 GCS（应保持 false） |

---

## 验收（本 Scaffold PR）

- [ ] `main` 上 Deck 生成回归无变化
- [ ] `REFRESH_ENABLED=false` 时用户界面与现网一致
- [ ] `scan_pptx()` 对非 zip 文件返回 `blocked` + `protected_file`
- [ ] `/api/config` 含 `refresh_enabled: false`

---

*后续 PR 在本分支上迭代，验证完成后再 merge `main`。*
