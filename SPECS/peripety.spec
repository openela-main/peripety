Name:           peripety
Version:        0.1.2
Release:        3%{?dist}
Summary:        Storage event notification daemon

Group:          System Environment/Daemons
License:        MIT
URL:            https://github.com/cathay4t/peripety
Source0:        https://github.com/cathay4t/peripety/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz
Patch0:         0001-Fix-compile-on-rust-1.20.0.patch
Patch1:         BZ_1656060_Replace-getmntent-with-thread-safe-libmount.patch
BuildRequires:  rust-toolset
BuildRequires:  systemd systemd-devel

%description
Peripety is designed to parse system storage logging into structured storage
event helping user investigate storage issues.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Source1 is vendored dependencies
%cargo_prep -V 1

%build
make

%post
%systemd_post peripetyd.service

%preun
%systemd_preun peripetyd.service

%postun
%systemd_postun_with_restart peripetyd.service

%install
%make_install

%files
%doc
%{_bindir}/prpt
%{_bindir}/peripetyd
%{_mandir}/man1/prpt.1*
%{_sysconfdir}/peripetyd.conf
%{_unitdir}/peripetyd.service

%changelog
* Mon Jan 14 2019 Gris Ge <fge@redhat.com> - 0.1.2-3
- Fix daemon crash casued by getmntent (RHBZ #1656060)

* Sat Dec 08 2018 Gris Ge <fge@redhat.com> - 0.1.2-2
- Use non-SCL way. (RHBZ #1657444)

* Tue Jun 05 2018 Gris Ge <fge@redhat.com> - 0.1.2-1
- Initial release.
