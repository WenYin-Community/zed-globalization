Name:           zedg
Version:        1.16.1
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
%attr(755, root, root) /usr/bin/zedg
%attr(755, root, root) /usr/libexec/zedg
/usr/share/applications/zedg.desktop
/usr/share/icons/hicolor/512x512/apps/zedg.png
/usr/share/icons/hicolor/1024x1024/apps/zedg.png
