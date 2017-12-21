%if 0%{?_no_wallet}
%define walletargs --disable-wallet
%define _buildqt 0
%define guiargs --with-gui=no
%else
%if 0%{?_no_gui}
%define _buildqt 0
%define guiargs --with-gui=no
%else
%define _buildqt 1
%define guiargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:    monero
Version: 0.11.1.0
Release: 1%{?dist}
Summary: Peer to Peer Cryptographic Currency
Group:   Applications/System
License: MIT
URL:     https://getmonero.org/
Source0: https://github.com/monero-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: unbound-devel
BuildRequires: openssl-devel
BuildRequires: pkg-config

%description
Monero is a p2p crytographic currency.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}

%check
ctest -V %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc LICENSE CONTRIBUTING.md README.md README.i18n.md VULNERABILITY_RESPONSE_PROCESS.md
%attr(0755,root,root) %{_bindir}/monerod
%attr(0755,root,root) %{_bindir}/monero-wallet-cli
%attr(0755,root,root) %{_bindir}/monero-wallet-rpc

%changelog
* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-1
- Initial build
