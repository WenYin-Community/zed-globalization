# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

zed-globalization (ZedG) 是 Zed 编辑器的多语言本地化工具链。通过 AI 驱动的全自动翻译流水线，将 Zed 源码中的英文 UI 字符串提取并翻译为中文/日语/韩语等，然后重新编译为本地化编辑器。

## 常用命令

### 安装
```bash
pip install .           # 基础安装
pip install ".[ai]"     # 含 AI 翻译功能 (openai, tiktoken)
pip install ".[all]"    # 全部功能 (含 pandas, openpyxl)
```

### CLI 工具 (zedl10n)
```bash
# 一键流水线 (推荐)
zedl10n pipeline --source-root zed --lang zh-CN --mode full

# 单步执行
zedl10n scan --source-root zed                          # AI 扫描待翻译文件
zedl10n extract --source-root zed --output string.json  # 提取字符串
zedl10n translate --input string.json --output i18n/zh-CN.json --mode full  # AI 翻译
zedl10n replace --input i18n/zh-CN.json --source-root zed  # 源码替换
zedl10n fix-placeholders --input i18n/zh-CN.json --source-root zed  # 修复占位符
zedl10n consistency --input i18n/zh-CN.json --fix       # 一致性检查
zedl10n convert to_excel --json i18n/zh-CN.json         # JSON -> Excel
zedl10n convert to_json --json i18n/zh-CN.json --excel translation.xlsx  # Excel -> JSON
zedl10n release-notes --version v0.228.0                # 翻译 Release Notes
```

### 品牌重命名
```bash
python scripts/rebrand.py <zed-source-root>   # Zed -> ZedG 重命名
```

### Agent 环境变量补丁
```bash
python patch_agent_env.py <zed-source-root>   # 修复 Claude Code 环境变量透传
```

## 架构

### 翻译流水线
```
scan (AI扫描) -> extract (正则提取) -> translate (AI翻译) -> replace (源码替换) -> 编译
```

### 核心模块 (src/zedl10n/)

| 模块 | 职责 |
|------|------|
| `cli.py` | CLI 入口，argparse 定义 9 个子命令 |
| `scan.py` | AI 扫描识别需翻译的 .rs 文件 (全量/增量) |
| `extract.py` | 正则提取双引号字符串 + 代码上下文 |
| `translate.py` | AI 并发翻译，三级降级策略 (JSON→XML CDATA→编号格式) |
| `replace.py` | 源码替换，三层保护 (过滤→受保护区域跳过→语法修正) |
| `batch.py` | Token 预算管理与批次拆分 |
| `prompts.py` | AI Prompt 模板和构建函数 |
| `consistency.py` | 翻译一致性检查与自动修复 |
| `fix_placeholders.py` | AI 修复占位符不匹配错误 |
| `convert.py` | JSON ↔ Excel 双向转换 |
| `release_notes.py` | Release Notes 获取与翻译 |
| `utils.py` | AIConfig, ProgressBar, JSON/XML/编号解析 |

### CI/CD 工作流 (.github/workflows/)

1. **01-translate.yml** - 定时(每日3次)+手动触发，检测 Zed 新版本 → AI 翻译 → 推送到 i18n 分支
2. **02-build.yml** - 由翻译工作流链式触发，6 并行构建矩阵 (Win/Linux/macOS × x64/ARM)
3. **03-update-scoop.yml** - Release 后更新 Windows Scoop Manifest
4. **04-update-homebrew.yml** - 构建完成后更新 macOS Homebrew Cask

### 配置文件

- `config/glossary.yaml` - 翻译术语表 (编辑器核心术语、应保留英文的专有名词)
- `config/crowdin.yml` - Crowdin 翻译平台配置

## 关键设计决策

### 翻译三级降级策略 (translate.py)
当 AI 无法正确返回 JSON 格式时，自动降级：JSON → XML CDATA → 编号格式，确保翻译始终可用。

### 源码替换三层保护 (replace.py)
1. **翻译过滤**: 跳过纯 ASCII 标点、纯小写标识符、占位符不匹配的条目
2. **受保护区域**: 跳过字节字符串 (`b""`/`br#""#`) 和属性宏 (`#[action(...)]`)
3. **语法修正**: 替换后自动将中文标点还原为 ASCII 标点

### 品牌重命名 (rebrand.py)
将上游 Zed 源码重命名为 ZedG，覆盖 SSH/Remote 二进制名、IPC 协议方案、Windows App 标识符、自动更新重定向等 7 个类别。

## 开发注意事项

- Python 3.11+，无自动化测试和 lint 配置
- 翻译依赖 OpenAI 兼容 API，需配置 `OPENAI_API_KEY` 等环境变量
- CI 构建使用 sccache 缓存 Rust 编译产物
- Linux 构建使用 mold 链接器 + clang 加速
- 术语表 (`config/glossary.yaml`) 控制翻译规范，修改前需理解其分类结构
