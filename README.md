# AI 智能体原理与 Vibe Coding 入门

一次面向 IT 部门（业务顾问 + 开发）的内部分享资料包。讲清 AI 是怎么工作的、Claude Code 这类工具怎么用才到位，并用一个**贯穿案例**演示一个真实需求从业务顾问到开发、AI 全程搭把手的完整流程。

## 仓库里有什么

| 资料 | 用途 | 文件 |
|------|------|------|
| 🎤 **演讲稿**（主线） | PPT 内容 + 讲师备注，上台直接用 | `docs/presentation_final.md` |
| 🎬 **演示脚本** | 案例四段操作 + 录屏兜底 + 翻车应对 | `docs/demo_scripts.md` |
| 📋 **课程纲要** | 讲师备课用的结构总览 | `docs/lesson_plan_summary.md` |
| 🔖 **提示词手册** | 课后参考：原则、模板、常见坑 | `docs/prompt_engineering_guide.md` |
| ⚡ **速查卡** | 课后参考：提示词 + 命令速查（业务/开发分栏） | `docs/quick_reference_guide.md` |
| 🧠 **原理补充** | 想深入了解 AI 原理可读 | `docs/ai_fundamentals_guide.md` |
| ✏️ **课后练习** | 上手试一遍 | `docs/exercises.md` |
| 💻 **案例代码** | 现场演示用的真实项目 | `src/` `tests/` |

另外 `docs/` 下还附了 BA/开发工作用的三个文档模板（需求文档、技术方案、测试用例）。

## 怎么用这套资料

- **要讲这场分享** → 从 `presentation_final.md`（讲稿）+ `demo_scripts.md`（演示脚本）开始
- **想快速了解讲了啥** → 看 `lesson_plan_summary.md`（纲要）
- **课后复习 / 日常使用** → `quick_reference_guide.md` + `prompt_engineering_guide.md`
- **想自己跑案例** → 见下方"案例代码"

## 内容结构（三段）

1. **原理**（~12–14 分钟）：AI 智能体 → 注意力机制 → 输入输出结构/上下文窗口 → 提示词 → 上下文工程/衰减 → 认知安全带
2. **工具**（~8–10 分钟）：什么是 Vibe Coding → Claude Code 不是聊天框 → CLAUDE.md → 协作姿势
3. **贯穿案例**（~15–20 分钟）：给员工信息管理加"按部门"，业务顾问段（需求澄清 / 文档产出）+ 开发段（功能实现 / 迭代纠错）一路打通

## 案例代码

现场演示围绕一个**真实的员工信息管理小项目**展开：

```
src/
├── models/user.py           # Pydantic 用户模型
├── services/user_service.py # 用户服务（含可重构点）
└── utils/validators.py      # 邮箱/密码/用户名校验
tests/
└── test_user_service.py     # 单元测试
```

案例演示：用 Claude Code 给 `User` 加 `department` 字段、加 `get_users_by_department` 和 `batch_import_users` 方法，并现场迭代纠错（`create_user` 的重复检查会抛 `ValueError`，贴报错让 AI 自修）。

### 跑起来

```bash
# 安装依赖
pip install -r requirements.txt

# 跑测试（案例演示的基线，需确保全绿）
pytest tests/ -v
```

> Python 3.10+，依赖 Pydantic v1、pytest。

## 环境要求

- Python 3.10+
- Claude Code CLI（用于现场演示；命令见 `docs/quick_reference_guide.md`）

## 许可证

MIT
