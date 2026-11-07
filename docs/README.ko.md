# ZedG — Zed 편집기 중국어 간체 버전

[![GitHub stars][stars-image]][stars-url]
[![Github Downloads][download-image]][download-url]
[![license][license-image]][license-url]

[简体中文](../README.md)|[English](README.en.md)|[日本語](README.ja.md)|**한국어**

[Zed 편집기](https://github.com/zed-industries/zed)의 중국어 간체 버전(현재 `zh-CN`만 배포). AI 기반의 완전 자동 번역 및 빌드 파이프라인: 업스트림 릴리스에서 번역 대상 문자열을 추출하고, AI로 번역한 뒤 소스를 치환하여 다시 빌드합니다.

> **참고:** 이 저장소는 COPR 및 AUR 패키징 전용입니다. Release 페이지에는 패키징에 필요한 `tar.gz` 소스만 게시합니다([WenYin-Community/ZedG](https://github.com/WenYin-Community/ZedG/releases/latest)에서 미러링). 그 외 플랫폼 설치 파일은 업스트림 저장소를 참조하세요.

## 특징

- **중국어 간체 UI**: 현재 `zh-CN`만 배포되며, 번역 엔진은 다국어 기능을 유지하여 추후 확장 가능
- AI 자동 스캔으로 번역 대상 Rust 소스 파일 식별
- 정규식 기반 문자열 추출 + 코드 컨텍스트 수집
- AI 동시 번역, 3단계 폴백 전략 (JSON -> XML CDATA -> 번호 형식)
- 소스 치환 3계층 보호 (필터링 + 구문 수정 + 보호 영역 건너뛰기)
- JSON <-> Excel 양방향 변환, 수동 검토 지원
- 크로스 플랫폼 빌드 (Windows / Linux / macOS), 앱 아이콘 포함
- GitHub Actions 완전 자동 파이프라인: 스캔 -> 번역 -> 빌드 -> 릴리스

## 자동화 파이프라인

```
05-sync-release (정시/수동)   업스트림 신규 릴리스 감지, tar.gz를 이 저장소 Release에 미러링,
                             패키징 파일 업데이트, COPR 빌드 트리거, AUR 푸시
```

## 로컬 사용

### 설치

```bash
# 기본 (치환 기능만)
pip install .

# AI 번역 기능 포함
pip install ".[ai]"

# 전체 기능
pip install ".[all]"
```

### 단계별 실행

```bash
# 1. AI 스캔: 번역이 필요한 .rs 파일 식별
zedl10n scan --source-root zed

# 2. 문자열 추출
zedl10n extract --source-root zed --output string.json

# 3. AI 번역
zedl10n translate --input string.json --output i18n/zh-CN.json --mode full

# 4. 소스 치환
zedl10n replace --input i18n/zh-CN.json --source-root zed
```

### 원클릭 파이프라인

```bash
zedl10n pipeline --source-root zed --lang zh-CN --mode full
```

### 로컬 빌드

```bash
git clone https://github.com/zed-industries/zed.git
zedl10n replace --input i18n/zh-CN.json --source-root zed
cd zed && cargo build --release
```

## AI 설정

| 환경 변수 | CLI 옵션 | 설명 | 기본값 |
|----------|----------|------|-------|
| `AI_BASE_URL` | `--base-url` | API 엔드포인트 | `https://api.openai.com/v1` |
| `AI_API_KEY` | `--api-key` | API 키 | 필수 |
| `AI_MODEL` | `--model` | 모델 이름 | `gpt-4o-mini` |
| `AI_CONCURRENCY` | `--concurrency` | 동시성 | `5` |

OpenAI 호환 API 지원. 우선순위: CLI 옵션 > 환경 변수 > 기본값.

## 프로젝트 구조

```
zed-globalization/
├── .github/workflows/
│   └── 05-sync-release.yml    # 업스트림 동기화 + COPR/AUR 패키징
├── config/
│   └── glossary.yaml       # 번역 용어집
├── i18n/                   # 번역 파일 (zh-CN)
├── src/zedl10n/
│   ├── cli.py              # CLI 엔트리 (scan/extract/translate/replace/convert/pipeline)
│   ├── scan.py             # AI 스캔
│   ├── extract.py          # 정규식 추출 + 컨텍스트
│   ├── translate.py        # AI 동시 번역 (3단계 폴백)
│   ├── replace.py          # 소스 치환 (3계층 보호)
│   ├── convert.py          # JSON <-> Excel 변환
│   └── utils.py            # 공유 유틸리티 및 설정
└── pyproject.toml
```

## 치환 보호 메커니즘

소스 치환 시 Rust 컴파일 안전성을 보장하는 다층 메커니즘:

1. **번역 필터링**: 순수 ASCII 구두점 문자열을 건너뛰어 배열 구문 파괴 방지
2. **보호 영역**: 바이트 문자열(`b""`/`br#""#`)과 속성 매크로(`#[action(...)]`) 내 치환 건너뛰기
3. **따옴표 이스케이프**: 번역문의 쌍따옴표를 자동으로 `\"`로 이스케이프
4. **구문 수정**: 문자열 사이의 중국어 구두점을 ASCII 구두점으로 자동 복원

## 감사의 말

- [Zed](https://github.com/zed-industries/zed)
- [deevus/zed-windows-builds](https://github.com/deevus/zed-windows-builds)
- [Nriver/zed-translation](https://github.com/Nriver/zed-translation)

## 라이선스

[MIT](../LICENSE)

[stars-url]: https://github.com/WenYin-Community/zed-globalization/stargazers
[stars-image]: https://img.shields.io/github/stars/WenYin-Community/zed-globalization?style=flat-square&logo=github
[download-url]: https://github.com/WenYin-Community/zed-globalization/releases/latest
[download-image]: https://img.shields.io/github/downloads/WenYin-Community/zed-globalization/total?style=flat-square&logo=github
[license-url]: https://github.com/WenYin-Community/zed-globalization/blob/main/LICENSE
[license-image]: https://img.shields.io/github/license/WenYin-Community/zed-globalization?style=flat-square
