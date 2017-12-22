Name:    monero
Version: 0.11.1.0
Release: 2%{?dist}
Summary: Peer to Peer Cryptographic Currency
Group:   Applications/System
License: MIT
URL:     https://getmonero.org/
Source0: https://github.com/monero-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:  https://raw.githubusercontent.com/eklitzke/monero-copr/master/monerod.service.patch

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: graphviz
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconf
BuildRequires: pkgconf-pkg-config

%description
Monero is a p2p crytographic currency.

%package static
Summary:        Peer to Peer Cryptographic Currency
Group:          Applications/System
BuildRequires: boost-static
BuildRequires: libstdc++-static

%description static

This package provides a statically linked build of Monero.

# FIXME: this is temporary
%global debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%patch0 -p0

%build
make %{?_smp_mflags} release-static

%check
#make %{?_smp_mflags} release-test

%install
mkdir -p %{buildroot}%{_sbindir}
install -p build/release/bin/* %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 600 utils/conf/monerod.conf %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 600 utils/systemd/monerod.service %{buildroot}%{_unitdir}/monerod.service

mkdir -p %{buildroot}%{_sharedstatedir}/monero

install -d %{buildroot}%{_localstatedir}/log/monero

%pre static
getent group monero >/dev/null || groupadd -r monero
getent passwd monero >/dev/null ||\
  useradd -r -g monero -d %{_sharedstatedir}/monero -s /sbin/nologin \
          -c "Monero wallet server" monero

%post static
%systemd_post monerod.service

%posttrans static
%{_bindir}/systemd-tmpfiles --create

%preun static
%systemd_preun bitcoind.service

%postun static
%systemd_postun bitcoind.service

%clean
rm -rf %{buildroot}

%files static
%defattr(-,root,root,-)
%license LICENSE
%doc LICENSE CONTRIBUTING.md README.md README.i18n.md VULNERABILITY_RESPONSE_PROCESS.md
%attr(0755,root,root) %{_sbindir}/monerod
%attr(0755,root,root) %{_sbindir}/monero-wallet-cli
%attr(0755,root,root) %{_sbindir}/monero-wallet-rpc
%attr(0755,root,root) %{_sbindir}/monero-blockchain-export
%attr(0755,root,root) %{_sbindir}/monero-blockchain-import
%attr(0644,root,root) %{_unitdir}/monerod.service
%attr(0700,monero,monero) %{_sharedstatedir}/monero
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/monerod.conf
%dir %attr(0750,monero,monero) %{_localstatedir}/log/monero

%changelog
* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-2
- Package for systemd with monerod user.

* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-1
- Initial build
