Name:           zedg
Version:        %{_zedg_version}
Release:        1%{?dist}
Summary:        Zed editor with globalization support
License:        AGPL-3.0-or-later AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://github.com/x6nux/zed-globalization

Source0:        https://github.com/x6nux/zed-globalization/releases/download/v%{_zedg_version}/zedg-%{_zedg_lang}-linux-%{_zedg_arch}-v%{_zedg_version}.tar.gz

AutoReqProv:    no

%description
A high-performance, multiplayer code editor with globalization support.
Pre-built binary from GitHub Releases.

%prep
# tar.gz 由 CI 生成，无需解压准备阶段

%install
mkdir -p %{buildroot}
tar -xzf %{SOURCE0} -C %{buildroot}

%files
%attr(755, root, root) /usr/bin/zedg
/usr/share/applications/zedg.desktop
/usr/share/icons/hicolor/512x512/apps/zedg.png
/usr/share/icons/hicolor/1024x1024/apps/zedg.png
