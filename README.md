# RepoPilot

[![CI](https://github.com/chenxiu9985/RepoPilot/actions/workflows/ci.yml/badge.svg)](https://github.com/chenxiu9985/RepoPilot/actions/workflows/ci.yml)

**Repository-Aware Coding Agent** — 面向本地 Python Git 仓库的问题定位、隔离修复与可复现验证。

## 当前状态

项目处于 **Phase 0：项目骨架**。目前提供可安装的 Python 包、CLI 帮助 / 版本入口、配置读取、自动化测试和 CI。

**尚未实现自动修复、LLM 调用、工具执行或 Docker 沙箱，也没有 benchmark 成绩。**
这些能力按 [路线图](docs/roadmap.md) 逐项开发；模块目录是职责边界，不代表功能已完成。

## 目标与边界

首版目标：输入本地 Git 仓库和明确的问题描述，检索相关代码，在独立工作区中生成补丁，在受限 Docker 环境运行 pytest，输出 Diff、测试结果与执行轨迹。

首版聚焦小型 Python 问题；不包含自动提交 PR、多 Agent、任意语言、分布式执行或复杂前端。

## 本地开发

需要 Python 3.11+ 和 Git。当前骨架不需要 API Key 或 Docker。

```text
git clone https://github.com/chenxiu9985/RepoPilot.git
cd RepoPilot
python -m venv .venv
```

Windows PowerShell（无需激活环境或修改执行策略）：

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]" -c requirements-dev.lock
.\.venv\Scripts\repopilot.exe --help
.\.venv\Scripts\repopilot.exe --version
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
```

Linux / macOS：

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]" -c requirements-dev.lock
repopilot --help
repopilot --version
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

`python -m repopilot` 也可以调用 CLI。`run` 命令尚未提供。
`requirements-dev.lock` 固定开发依赖版本，更新流程见 [贡献指南](CONTRIBUTING.md)。

若本机配置的镜像源连接失败，可在安装命令末尾添加 `--index-url https://pypi.org/simple`，仅影响该次安装。

## 配置

可复制 `.env.example` 为 `.env`。环境变量使用 `REPOPILOT_` 前缀，优先级为：显式参数 > 环境变量 > `.env` > 默认值。

模型地址、模型名和密钥目前允许为空。步数 / 超时必须为正数，重试次数为 0～5。配置中的限制值将在对应执行模块实现后生效；当前仅校验配置。

密钥字段从配置的常规序列化和 repr 中排除；这不代替未来日志模块的脱敏工作。不要提交 `.env`、运行日志或私人目标仓库。

## 目录

```text
src/repopilot/
  cli.py          CLI 帮助与版本入口
  config.py       Pydantic 配置读取与校验
  agent/          待实现：任务状态与 Agent Loop
  llm/            待实现：模型接口、Fake 与 API 适配器
  tools/          待实现：工具注册、读取、搜索、补丁与 Diff
  sandbox/        待实现：独立工作区与 Docker 执行
tests/            配置边界与已安装 CLI 的测试
docs/             架构、路线图与设计决策
examples/         后续可复现案例的约定
.github/          CI、Issue 与 PR 模板
```

## 开发与项目管理

- 从 [Issues](https://github.com/chenxiu9985/RepoPilot/issues) 选择一个验收条件明确的任务。
- 创建短期功能分支，完成实现和测试，再通过 PR 合并到 `main`。
- 通过 [Milestones](https://github.com/chenxiu9985/RepoPilot/milestones) 管理 Phase 0～4。
- CI 在 Windows / Linux、Python 3.11 / 3.12 上检查安装、Ruff、pytest 和打包。
- 真实模型实验与日常测试分开，结果必须来自实际执行。

详见 [贡献指南](CONTRIBUTING.md)、[架构设计](docs/architecture.md) 和 [路线图](docs/roadmap.md)。

## License

[MIT](LICENSE)
