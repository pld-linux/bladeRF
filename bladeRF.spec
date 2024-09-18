# TODO:
# - -DENABLE_FX3_BUILD (requires arm toolchain)
# - host/libraries/libbladeRF_bindings
Summary:	Library and tools to interact with bladeRF platform
Summary(pl.UTF-8):	Biblioteka i narzędzia do pracy z platformą bladeRF
Name:		bladeRF
Version:	2024.05
Release:	1
License:	LGPL v2.1, GPL v2, MIT
Group:		Applications/Communication
#Source0Download: https://github.com/Nuand/bladeRF/releases
Source0:	https://github.com/Nuand/bladeRF/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	63bc0e0896b08f105f30722f82ee9eb8
%define	noOS_gitref	0bba46e6f6f75785a65d425ece37d0a04daf6157
Source1:	https://github.com/analogdevicesinc/no-OS/archive/%{noOS_gitref}/no-OS-%{noOS_gitref}.tar.gz
# Source1-md5:	2c06ff9297d8beb0482a1b0b5e4d3128
URL:		https://github.com/Nuand/bladeRF
BuildRequires:	cmake >= 3.5
# or libedit (libtecla preferred)
BuildRequires:	libtecla-devel
BuildRequires:	libusb-devel >= 1.0.16
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library and tools to interact with bladeRF platform.

%description -l pl.UTF-8
Biblioteka i narzędzia do pracy z platformą bladeRF.

%package libs
Summary:	Library to interact with the bladeRF device
Summary(pl.UTF-8):	Biblioteka do współpracy z urządzeniami bladeRF
Group:		Libraries
Requires:	libusb >= 1.0.16

%description libs
Library to interact with the bladeRF device.

%description libs -l pl.UTF-8
Biblioteka do współpracy z urządzeniami bladeRF.

%package devel
Summary:	Header files for libbladeRF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbladeRF
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for libbladeRF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbladeRF.

%prep
%setup -q

%{__tar} xf %{SOURCE1} -C thirdparty/analogdevicesinc/no-OS --strip-components=1

%build
install -d host/build
cd host/build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DUDEV_RULES_PATH=/lib/udev/rules.d \
	-DVERSION_INFO_EXTRA=""

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# cmake script defaults to %{_prefix}/lib if libdir doesn't exists
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} -C host/build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG CONTRIBUTORS COPYING README.md
%attr(755,root,root) %{_bindir}/bladeRF-cli
%attr(755,root,root) %{_bindir}/bladeRF-fsk
/lib/udev/rules.d/88-nuand-bladerf1.rules
/lib/udev/rules.d/88-nuand-bladerf2.rules
/lib/udev/rules.d/88-nuand-bootloader.rules

%files libs
%defattr(644,root,root,755)
%doc host/libraries/libbladeRF/{CHANGELOG,README.md}
%attr(755,root,root) %{_libdir}/libbladeRF.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbladeRF.so
%{_includedir}/bladeRF1.h
%{_includedir}/bladeRF2.h
%{_includedir}/libbladeRF.h
%{_pkgconfigdir}/libbladeRF.pc
%{_datadir}/cmake/bladeRF
