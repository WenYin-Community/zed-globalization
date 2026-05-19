#!/usr/bin/env bash
# 从 GitHub Releases 自动获取最新版本并构建 RPM
set -euo pipefail

REPO="x6nux/zed-globalization"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SPEC_FILE="$SCRIPT_DIR/zedg-from-release.spec"

# 默认值
LANG="${1:-zh-cn}"

echo ">>> 获取最新版本..."
LATEST=$(curl -sf "https://api.github.com/repos/${REPO}/releases/latest" | jq -r '.tag_name')
if [ -z "$LATEST" ] || [ "$LATEST" = "null" ]; then
  echo "错误: 无法获取最新版本" >&2
  exit 1
fi
VERSION="${LATEST#v}"
echo ">>> 最新版本: $LATEST (v前缀去除后: $VERSION)"

build_rpm() {
  local arch="$1"
  local target="$2"
  echo ""
  echo "========================================="
  echo "  构建 $arch RPM (版本 $VERSION)"
  echo "========================================="
  rpmbuild -bb "$SPEC_FILE" \
    --define "_zedg_version $VERSION" \
    --define "_zedg_arch $arch" \
    --define "_zedg_lang $LANG" \
    --target "$target"
}

build_rpm x86_64  x86_64
build_rpm aarch64 aarch64

echo ""
echo ">>> 构建完成，RPM 产物:"
find ~/rpmbuild/RPMS/ -name "zedg-*.rpm" -ls 2>/dev/null || \
  find "$HOME/rpmbuild/RPMS/" -name "zedg-*.rpm" -ls 2>/dev/null || \
  echo "请检查 ~/rpmbuild/RPMS/ 目录"
