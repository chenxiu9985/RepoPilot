# 开发协作

## 日常流程

1. 从 Issue 开始，写清目标、范围、验收标准与验证方式。
2. 从最新 `main` 创建短期分支，例如 `codex/agent-state`。
3. 先解释关键设计，再实现；一个任务通常控制在半天到两天。
4. 在项目虚拟环境运行 Ruff、pytest，阅读 Diff 后提交。
5. 推送功能分支并创建 PR，关联 Issue，记录实际验证和限制。
6. 检查 CI，合并后关闭任务；独立开发可自己审阅和合并。

首次初始化直接建立 `main`；后续功能使用上述流程。不需要长期 `develop` 分支。

建议看板状态：待考虑 → 待开发 → 开发中 → 待验收 → 已完成。
开发中尽量只有一个主要任务；每周调整近期任务，后续 Phase 保留概要。

## 完成标准

- Issue 的可验证条件得到满足，包括与改动相关的失败路径。
- 代码可安装，相关测试和检查通过。
- 使用方式变化时同步文档。
- 提交中没有密钥、私人仓库或无关生成文件。
- 明确区分 Fake/Mock 流程验证与真实模型 / Docker 的修复结果。

## 检查与构建

先按 README 创建开发环境。以下命令使用该环境中的 Python：

```text
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m build
python -m pip check
```

格式修正可执行 `python -m ruff format .`。测试直接定位当前 Python 环境中的已安装 CLI，无需修改系统 PATH。

## 更新依赖

`pyproject.toml` 声明兼容范围；`requirements-dev.lock` 是固定版本的开发依赖快照，作为 pip constraints 使用，包含传递依赖。它不是带哈希的跨平台锁文件，也不固定隔离构建环境里的构建工具版本。

更新时在干净的临时虚拟环境中，不带旧 constraints 安装 `.[dev]`，然后使用 `python -m pip freeze --exclude-editable` 生成新快照，移除只适用于生成平台的依赖或为其添加正确的环境标记。提交前必须通过 CI 的 Windows / Linux 和 Python 3.11 / 3.12 检查。

只在明确的依赖更新任务中刷新快照，避免普通功能开发悄悄升级依赖。

## 实验记录

后续真实模型实验记录：代码提交、目标仓库初始提交、任务集版本、模型与供应商标识、配置、工具调用、测试结果、耗时及可获得的 token 用量。保存可公开复现的脱敏结果；不发布凭据或原始私人仓库。
