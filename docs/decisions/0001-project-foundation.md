# ADR 0001：项目基础与开发流程

日期：2026-11-11。状态：采用。

## 背景

个人开发的 Python Coding Agent 需要可安装、可验证、可追踪的起点，并支持后续安全执行与评测。

## 决策

- 使用 Python 3.11+、src 布局、pyproject.toml 和 Hatchling 构建。
- 本地使用 venv + pip；固定开发依赖快照，无需额外包管理器。
- 配置采用 Pydantic Settings，CLI 暂用标准库 argparse。
- 日常检查使用 Ruff 和 pytest，CI 覆盖 Windows / Linux 的 Python 3.11 / 3.12。
- 本地开发，GitHub 保存代码与任务；初始提交建立 main，后续使用短期分支和 PR。
- 采用 MIT 许可证。
- 核心 Agent Loop 自主实现；当前不加入 Agent 框架、数据库或 Web 服务。

## 取舍

src 布局要求先安装再测试，但可以及早暴露打包与入口问题。argparse 满足当前命令数量，后续按实际交互复杂度评估。
依赖快照控制应用和开发依赖版本；没有宣称完整环境按位复现，构建工具与跨平台解释器仍需 CI 验证。
保留少量模块边界目录，不实现没有调用者的通用抽象。
