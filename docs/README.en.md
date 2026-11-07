# ZedG — Simplified Chinese Edition of Zed

[![GitHub stars][stars-image]][stars-url]
[![Github Downloads][download-image]][download-url]
[![license][license-image]][license-url]

[简体中文](../README.md)|**English**|[日本語](README.ja.md)|[한국어](README.ko.md)

Simplified Chinese build of the [Zed Editor](https://github.com/zed-industries/zed) (only `zh-CN` is currently published). AI-driven, fully automated translation and build pipeline: extract translatable strings from each upstream release, translate with AI, patch the source and rebuild out of the box.

> **Note:** This repository is only used for COPR and AUR packaging. The Release page only hosts the `tar.gz` sources required for packaging (mirrored from [WenYin-Community/ZedG](https://github.com/WenYin-Community/ZedG/releases/latest)); installers for other platforms are available upstream.

## Features

- **Simplified Chinese UI**: only `zh-CN` is published for now; the translation engine keeps multi-language capability and can be extended later
- AI-powered scanning to identify translatable Rust source files
- Regex-based string extraction with code context collection
- Concurrent AI translation with 3-level fallback (JSON -> XML CDATA -> numbered format)
- Source replacement with 3-layer protection (filtering + syntax repair + protected region skipping)
- Bidirectional JSON <-> Excel conversion for manual review
- Cross-platform builds (Windows / Linux / macOS) with app icons
- Fully automated GitHub Actions pipeline: scan -> translate -> build -> release

## Automation Pipeline

```
05-sync-release (cron/manual)   Detect new upstream release, mirror tar.gz to this repo's Release,
                                update packaging files, trigger COPR build, push to AUR
```

## Local Usage

### Install

```bash
# Basic (replacement only)
pip install .

# With AI translation
pip install ".[ai]"

# All features
pip install ".[all]"
```

### Step by Step

```bash
# 1. AI scan: identify .rs files needing translation
zedl10n scan --source-root zed

# 2. Extract strings
zedl10n extract --source-root zed --output string.json

# 3. AI translate
zedl10n translate --input string.json --output i18n/zh-CN.json --mode full

# 4. Replace source
zedl10n replace --input i18n/zh-CN.json --source-root zed
```

### One-click Pipeline

```bash
zedl10n pipeline --source-root zed --lang zh-CN --mode full
```

### Local Build

```bash
git clone https://github.com/zed-industries/zed.git
zedl10n replace --input i18n/zh-CN.json --source-root zed
cd zed && cargo build --release
```

## AI Configuration

| Env Variable | CLI Flag | Description | Default |
|-------------|----------|-------------|---------|
| `AI_BASE_URL` | `--base-url` | API endpoint | `https://api.openai.com/v1` |
| `AI_API_KEY` | `--api-key` | API key | Required |
| `AI_MODEL` | `--model` | Model name | `gpt-4o-mini` |
| `AI_CONCURRENCY` | `--concurrency` | Concurrency | `5` |

Compatible with any OpenAI-compatible API. Priority: CLI flag > env variable > default.

## Project Structure

```
zed-globalization/
├── .github/workflows/
│   └── 05-sync-release.yml    # Upstream sync + COPR/AUR packaging
├── config/
│   └── glossary.yaml       # Translation glossary
├── i18n/                   # Translation files (zh-CN)
├── src/zedl10n/
│   ├── cli.py              # CLI entry (scan/extract/translate/replace/convert/pipeline)
│   ├── scan.py             # AI scan for translatable files
│   ├── extract.py          # Regex string extraction + context
│   ├── translate.py        # Concurrent AI translation (3-level fallback)
│   ├── replace.py          # Source replacement (3-layer protection)
│   ├── convert.py          # JSON <-> Excel conversion
│   └── utils.py            # Shared utilities and config
└── pyproject.toml
```

## Replacement Protection

Multiple layers ensure Rust compilation safety during source replacement:

1. **Translation filtering**: Skip pure ASCII punctuation strings to preserve array syntax
2. **Protected regions**: Skip byte strings (`b""`/`br#""#`) and attribute macros (`#[action(...)]`)
3. **Quote escaping**: Auto-escape double quotes in translations to `\"`
4. **Syntax repair**: Auto-restore Chinese punctuation between strings to ASCII equivalents

## Acknowledgements

- [Zed](https://github.com/zed-industries/zed)
- [deevus/zed-windows-builds](https://github.com/deevus/zed-windows-builds)
- [Nriver/zed-translation](https://github.com/Nriver/zed-translation)

## License

[MIT](../LICENSE)

[stars-url]: https://github.com/WenYin-Community/zed-globalization/stargazers
[stars-image]: https://img.shields.io/github/stars/WenYin-Community/zed-globalization?style=flat-square&logo=github
[download-url]: https://github.com/WenYin-Community/zed-globalization/releases/latest
[download-image]: https://img.shields.io/github/downloads/WenYin-Community/zed-globalization/total?style=flat-square&logo=github
[license-url]: https://github.com/WenYin-Community/zed-globalization/blob/main/LICENSE
[license-image]: https://img.shields.io/github/license/WenYin-Community/zed-globalization?style=flat-square
