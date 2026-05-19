#!/usr/bin/env python3
"""
Patch script: force file-based credential storage.

Replaces the keychain-based credential provider logic so that all release
channels always use local file storage. This avoids macOS Keychain prompts
on every launch for self-signed (ad-hoc) builds.

Usage:
    python3 scripts/patch_file_credentials.py [--zed-dir ./zed]
"""

import argparse
import sys
from pathlib import Path

TARGET_FILE = (
    "crates/zed_credentials_provider/src/zed_credentials_provider.rs"
)

OLD_FN = """\
fn new(cx: &App) -> Arc<dyn CredentialsProvider> {
    let use_development_provider = match ReleaseChannel::try_global(cx) {
        Some(ReleaseChannel::Dev) => {
            // In development we default to using the development
            // credentials provider to avoid getting spammed by relentless
            // keychain access prompts.
            //
            // However, if the `ZED_DEVELOPMENT_USE_KEYCHAIN` environment
            // variable is set, we will use the actual keychain.
            !*ZED_DEVELOPMENT_USE_KEYCHAIN
        }
        Some(ReleaseChannel::Nightly | ReleaseChannel::Preview | ReleaseChannel::Stable) | None => {
            false
        }
    };

    if use_development_provider {
        Arc::new(DevelopmentCredentialsProvider::new())
    } else {
        Arc::new(KeychainCredentialsProvider)
    }
}"""

NEW_FN = """\
fn new(_cx: &App) -> Arc<dyn CredentialsProvider> {
    Arc::new(DevelopmentCredentialsProvider::new())
}"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zed-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "zed",
        help="Path to the zed source directory (default: ./zed)",
    )
    args = parser.parse_args()

    target = args.zed_dir / TARGET_FILE
    if not target.exists():
        print(f"[ERROR] Target file not found: {target}", file=sys.stderr)
        return 1

    content = target.read_text(encoding="utf-8")

    if NEW_FN in content:
        print("[OK] Already patched, skipping.")
        return 0

    if OLD_FN not in content:
        print(
            f"[ERROR] Cannot find expected code block in {TARGET_FILE}.\n"
            "The upstream source may have changed. Manual update needed.",
            file=sys.stderr,
        )
        return 1

    content = content.replace(OLD_FN, NEW_FN)
    target.write_text(content, encoding="utf-8")
    print("[OK] Patched: credentials provider now uses file storage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
