Name:    monero
Version: 0.11.1.0
Release: 1%{?dist}
Summary: Peer to Peer Cryptographic Currency
Group:   Applications/System
License: MIT
URL:     https://getmonero.org/
Source0: https://github.com/monero-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

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
%setup -q

%build
make %{?_smp_mflags} release-static

%check
#make %{?_smp_mflags} release-test

%install
mkdir -p %{buildroot}%{_sbindir}
install -p build/release/bin/* %{buildroot}%{_sbindir}

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

%changelog
* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-1
- Initial build
