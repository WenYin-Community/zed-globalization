Name:           zedg
Version:        1.22.0
Release:        1%{?dist}
Summary:        Zed editor with globalization support
License:        AGPL-3.0-or-later AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://github.com/WenYin-Community/zed-globalization

Source0:        https://github.com/WenYin-Community/zed-globalization/releases/download/v%{version}/zedg-zh-cn-linux-x86_64-v%{version}.tar.gz
Source1:        https://github.com/WenYin-Community/zed-globalization/releases/download/v%{version}/zedg-zh-cn-linux-aarch64-v%{version}.tar.gz

AutoReqProv:    no

%description
A high-performance, multiplayer code editor with globalization support.
Pre-built binary from GitHub Releases.

%install
mkdir -p %{buildroot}
%ifarch x86_64
tar -xzf %{SOURCE0} -C %{buildroot}
%else
tar -xzf %{SOURCE1} -C %{buildroot}
%endif

%files
# 清单必须与 CI 打出的 tar.gz 布局保持一致，新增/删除文件时同步更新
%attr(755, root, root) /usr/bin/zedg
%attr(755, root, root) /usr/bin/zedg-activate
%attr(755, root, root) /usr/libexec/zedg
# 生态兼容软链（issue #37）
/usr/bin/zed
/usr/libexec/zed-cli
%dir /usr/lib/zedg
/usr/lib/zedg/libgit2.so.*
/usr/share/applications/zedg.desktop
/usr/share/icons/hicolor/512x512/apps/zedg.png
/usr/share/icons/hicolor/1024x1024/apps/zedg.png
