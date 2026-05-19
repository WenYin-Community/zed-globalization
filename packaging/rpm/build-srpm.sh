#!/usr/bin/env bash
# 在 COPR 构建环境中运行：获取最新版本，生成 SRPM
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SPEC_TEMPLATE="$SCRIPT_DIR/zedg-copr.spec"

# 获取最新版本
LATEST=$(curl -sf https://api.github.com/repos/x6nux/zed-globalization/releases/latest | jq -r '.tag_name')
VERSION="${LATEST#v}"
echo ">>> 最新版本: $VERSION"

# 生成硬编码版本的 spec
SPEC_OUT="$SCRIPT_DIR/zedg.spec"
sed "s/%(curl.*$/Version:        $VERSION/" "$SPEC_TEMPLATE" > "$SPEC_OUT"

rpmbuild -bs "$SPEC_OUT"
