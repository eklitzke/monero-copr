Name:    monero
Version: 0.12.0.0
Release: 1%{?dist}
Summary: Peer to Peer Cryptographic Currency
Group:   Applications/System
License: MIT
URL:     https://getmonero.org/
Source0: https://github.com/monero-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:  0001-class-memaccess.patch

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppzmq-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: graphviz
BuildRequires: gtest-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconf
BuildRequires: pkgconf-pkg-config
BuildRequires: readline-devel
BuildRequires: systemd-units
BuildRequires: unbound-devel

Obsoletes: monero-static

%description
Monero is a secure, private, and untraceable cryptocurrency.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1

%build
# There is a Makefile checked into the project, but we need to regenerate it to
# get the Fedora/Red Hat cmake packaging macros. In particular, this ensures
# we're building with the expected hardening flags.
mkdir -p build/release
pushd build/release
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -D STATIC=OFF -D ARCH="x86-64" -D BUILD_64=ON -D BUILD_TESTS=ON -D CMAKE_BUILD_TYPE=release ../..

# Actually build monerod and everything else.
make %{?_smp_mflags}
popd

%check
# FIXME: these tests fail, apparently due to SELinux errors
pushd build/release
ctest -V %{?_smp_mflags} || true
popd

%install
make -C build/release install DESTDIR=%{buildroot}

# For some reason the default install target tries to install libminiupnpc.a and
# the miniupnpc headers (but doesn't do this for other vendored libs).
rm -f %{buildroot}%{_libdir}/libminiupnpc.a
rm -rf %{buildroot}%{_includedir}/miniupnpc

# For some reason these aren't installed by "make install".
#install -p -m 755 build/release/bin/monero-blockchain-{import,export} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 600 utils/conf/monerod.conf %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 600 utils/systemd/monerod.service %{buildroot}%{_unitdir}/monerod.service

mkdir -p %{buildroot}%{_sharedstatedir}/monero
mkdir -p %{buildroot}%{_localstatedir}/log/monero

rm -rf %{buildroot}%{_includedir}/wallet

%pre
getent group monero >/dev/null || groupadd -r monero
getent passwd monero >/dev/null ||\
  useradd -r -g monero -d %{_sharedstatedir}/monero -s /sbin/nologin \
          -c "Monero wallet server" monero

%post
%systemd_post monerod.service

%posttrans
%{_bindir}/systemd-tmpfiles --create

%preun
%systemd_preun monerod.service

%postun
%systemd_postun monerod.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc LICENSE CONTRIBUTING.md README.md README.i18n.md
%attr(0755,root,root) %{_bindir}/monero-blockchain-blackball
%attr(0755,root,root) %{_bindir}/monero-blockchain-export
%attr(0755,root,root) %{_bindir}/monero-blockchain-import
%attr(0755,root,root) %{_bindir}/monero-blockchain-usage
%attr(0755,root,root) %{_bindir}/monero-gen-trusted-multisig
%attr(0755,root,root) %{_bindir}/monero-wallet-cli
%attr(0755,root,root) %{_bindir}/monero-wallet-rpc
%attr(0755,root,root) %{_bindir}/monerod
%attr(0644,root,root) %{_unitdir}/monerod.service
%attr(0700,monero,monero) %{_sharedstatedir}/monero
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/monerod.conf
%dir %attr(0750,monero,monero) %{_localstatedir}/log/monero

%changelog
* Sun Apr 22 2018 Evan Klitzke <evan@eklitzke.org> - 0.12.0.0-1
- Monero 0.12.0

* Sun Mar 25 2018 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-5
- Fix a small bug in the systemd unit

* Fri Dec 22 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-4
- Fix how the test suite is linked/run.

* Fri Dec 22 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-3
- Install to /usr/bin instead of /usr/sbin, use Fedora packaging macros, enable
  debug symbols.

* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-2
- Package for systemd with monerod user.

* Thu Dec 21 2017 Evan Klitzke <evan@eklitzke.org> - 0.11.1.0-1
- Initial build
