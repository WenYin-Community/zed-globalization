# ZedG — Zed 编辑器简体中文版

[![GitHub stars][stars-image]][stars-url]
[![Github Downloads][download-image]][download-url]
[![license][license-image]][license-url]

> **⚠️ 说明：** 本仓库仅用于 COPR 和 AUR 打包推送。Release 页面只放打包所需的 `tar.gz` 源文件（从 [wenyinos/ZedG](https://github.com/wenyinos/ZedG/releases/latest) 镜像备份），其他平台安装包请访问上游仓库。
> 每 1 天自动检测上游新版本并同步打包。全部历史版本资产与校验和见 [RELEASES.md](RELEASES.md)。

### COPR (Fedora/RHEL)

- **架构支持**：x86_64 / aarch64（workflow 按 Fedora 43/44、RHEL 10 的多架构矩阵构建）
- **构建触发**：由 workflow 自动触发，无需手动操作
- **安装方式**：
  ```bash
  # 启用 COPR 仓库
  dnf copr enable ruojiner/zedg
  # 安装
  dnf install zedg
  ```

### AUR (Arch Linux)

- **架构支持**：支持 x86_64 和 aarch64（通过 PKGBUILD 的 `source_x86_64`/`source_aarch64` 分别指定）
- **构建触发**：由 workflow 自动推送到 AUR
- **安装方式**：
  ```bash
  # 使用 yay
  yay -S zedg
  # 或使用 paru
  paru -S zedg
  ```

[Zed 编辑器](https://github.com/zed-industries/zed) 的简体中文版（当前仅发布 `zh-CN`）。AI 驱动的全自动翻译与构建流水线：跟随上游版本自动提取待译字符串、AI 翻译、替换源码并重新编译，开箱即用。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WenYin-Community/zed-globalization&type=Date)](https://star-history.com/#WenYin-Community/zed-globalization&Date)

> **Zed 汉化版** | Zed 简体中文版 | Zed 中文版 | Zed Chinese | Zed Simplified Chinese | Zed Localized | Zed i18n | Zed l10n

## 特性

- **简体中文界面**：当前发布语言为 `zh-CN`，翻译引擎保留多语言能力，后续可按需扩展
- AI 自动扫描识别需翻译的 Rust 源文件
- 正则提取双引号字符串 + 代码上下文收集
- AI 并发翻译，三级降级策略（JSON -> XML CDATA -> 编号格式）
- 源码替换三层保护（过滤 + 语法修正 + 受保护区域跳过）
- JSON <-> Excel 双向转换，支持人工校对
- 跨平台构建（Windows / Linux / macOS），含应用图标
- GitHub Actions 全自动流水线：扫描 -> 翻译 -> 构建 -> 发布

## 自动化流水线

```
05-sync-release (每天定时/手动)  检测上游新版本 → 下载 tar.gz 到本仓库 Release（备份）→ 更新打包文件 → 触发 COPR 构建 → 推送 AUR
```

## 本地使用

### 安装工具

```bash
# 基础安装（仅替换功能）
pip install .

# 含 AI 翻译功能
pip install ".[ai]"

# 全部功能
pip install ".[all]"
```

### 分步执行

```bash
# 1. AI 扫描：识别哪些 .rs 文件需要翻译
zedl10n scan --source-root zed

# 2. 提取字符串
zedl10n extract --source-root zed --output string.json

# 3. AI 翻译
zedl10n translate --input string.json --output i18n/zh-CN.json --mode full

# 4. 替换源码
zedl10n replace --input i18n/zh-CN.json --source-root zed
```

### 一键流水线

```bash
zedl10n pipeline --source-root zed --lang zh-CN --mode full
```

### 本地构建

```bash
git clone https://github.com/zed-industries/zed.git
zedl10n replace --input i18n/zh-CN.json --source-root zed
python3 patch_agent_env.py --source-root zed
cd zed && cargo build --release
```

> **`patch_agent_env.py` 补丁说明：** Zed 源码中 `agent_server_store.rs` 会强制将 `ANTHROPIC_API_KEY` 设为空字符串，导致用户系统中已配置的 API Key 被清除；同时 `claude.rs` 的 `connect()` 方法没有像 Codex/Gemini 那样从系统环境变量读取并透传 API Key。该补丁自动修复这两个问题：
> - **补丁 1**：删除 `agent_server_store.rs` 中 `env.insert("ANTHROPIC_API_KEY", "")` 的强制清空行
> - **补丁 2**：在 `claude.rs` 的 `connect()` 中注入环境变量透传逻辑，将 `ANTHROPIC_API_KEY`、`ANTHROPIC_BASE_URL`、Bedrock/Vertex 相关变量及 `AWS_*`、`GOOGLE_CLOUD_*` 前缀变量传递给 Claude Code 进程
>
> 脚本幂等安全：通过 `[ZED_GLOBALIZATION_PATCH]` 标记检测是否已打补丁，重复运行自动跳过。支持 `--dry-run` 仅预览不修改。

## AI 配置

| 环境变量 | CLI 参数 | 说明 | 默认值 |
|----------|----------|------|--------|
| `AI_BASE_URL` | `--base-url` | API 地址 | `https://api.openai.com/v1` |
| `AI_API_KEY` | `--api-key` | API 密钥 | 无（必填） |
| `AI_MODEL` | `--model` | 模型名称 | `gpt-4o-mini` |
| `AI_CONCURRENCY` | `--concurrency` | 并发数 | `5` |

支持任何 OpenAI 兼容 API。优先级：CLI 参数 > 环境变量 > 默认值。

## 项目结构

```
zed-globalization/
├── .github/workflows/
│   └── 05-sync-release.yml    # 上游同步 + COPR/AUR 打包
├── config/
│   └── glossary.yaml       # 翻译术语表
├── i18n/                   # 翻译文件（zh-CN）
├── src/zedl10n/
│   ├── cli.py              # CLI 入口（scan/extract/translate/replace/convert/pipeline）
│   ├── scan.py             # AI 扫描识别待翻译文件
│   ├── extract.py          # 正则提取字符串 + 上下文
│   ├── translate.py        # AI 并发翻译（三级降级）
│   ├── replace.py          # 源码替换（多级路径解析 + 三层保护）
│   ├── convert.py          # JSON <-> Excel 转换
│   └── utils.py            # 共享工具与配置
├── patch_agent_env.py      # 编译前补丁：修复 Agent 环境变量透传
└── pyproject.toml
```

## 替换保护机制

源码替换时通过多层机制保障 Rust 编译安全：

1. **翻译过滤**：跳过纯 ASCII 标点字符串，避免破坏数组语法
2. **受保护区域**：跳过字节字符串（`b""`/`br#""#`）和属性宏（`#[action(...)]`）内的替换
3. **引号转义**：译文中的双引号自动转义为 `\"`
4. **语法修正**：替换后自动将字符串间的中文标点（`、`/`，`/`；`）还原为 ASCII 标点

## 鸣谢

- [Zed](https://github.com/zed-industries/zed)
- [deevus/zed-windows-builds](https://github.com/deevus/zed-windows-builds)
- [Nriver/zed-translation](https://github.com/Nriver/zed-translation)

## 许可证

[MIT](LICENSE)

[stars-url]: https://github.com/WenYin-Community/zed-globalization/stargazers
[stars-image]: https://img.shields.io/github/stars/WenYin-Community/zed-globalization?style=flat-square&logo=github
[download-url]: https://github.com/WenYin-Community/zed-globalization/releases/latest
[download-image]: https://img.shields.io/github/downloads/WenYin-Community/zed-globalization/total?style=flat-square&logo=github
[license-url]: https://github.com/WenYin-Community/zed-globalization/blob/main/LICENSE
[license-image]: https://img.shields.io/github/license/WenYin-Community/zed-globalization?style=flat-square

---

<details>
<summary>关键词 / Keywords</summary>

Zed 汉化版, Zed 中文版, Zed 简体中文版, Zed 编辑器汉化, Zed 编辑器中文版, Zed 编辑器中文, Zed 中文汉化,
Zed 简体中文, Zed 本地化, Zed 翻译,
Zed Chinese, Zed Simplified Chinese, Zed Localized, Zed Globalization,
Zed i18n, Zed l10n, Zed Translation, Zed Editor Chinese, Zed Editor Localized,
Zed 代替 VSCode, Zed 代替 Cursor, Rust 编辑器中文版, 高性能编辑器汉化

</details>
