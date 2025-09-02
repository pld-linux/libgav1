#
# Conditional build:
%bcond_without	tests	# tests building

Summary:	AV1 decoder library (10-bit)
Summary(pl.UTF-8):	Biblioteka dekodera AV1 (10-bitowego)
Name:		libgav1
Version:	0.20.0
Release:	2
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://chromium.googlesource.com/codecs/libgav1
#Source0:	https://chromium.googlesource.com/codecs/libgav1/+archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# tarball is recreated on each download, so upload via dropin
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	467d48d1107e8a129425336d5a87e66c
Patch0:		%{name}-system-libs.patch
Patch1:		cxx17.patch
Patch2:		%{name}-sse4-tests.patch
URL:		https://chromium.googlesource.com/codecs/libgav1
BuildRequires:	abseil-cpp-devel
BuildRequires:	cmake >= 3.7.1
BuildRequires:	gtest-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgav1 is a Main profile (0) & High profile (1) compliant AV1
decoder.

%description -l pl.UTF-8
libgav1 to dekoder AV1 zgodny z profilami Main (0) i High (1).

%package devel
Summary:	Header files for libgav1 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgav1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for libgav1 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgav1.

%package static
Summary:	Static libgav1 library
Summary(pl.UTF-8):	Statyczna biblioteka libgav1
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgav1 library.

%description static -l pl.UTF-8
Statyczna biblioteka libgav1.

%prep
%setup -q -c
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_DATAROOTDIR=share \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{!?with_tests:-DLIBGAV1_ENABLE_TESTS=OFF}

%{__make}

%if %{with tests}
# how to execute all automatically?
for f in $(echo ./*_test) ; do
	if [ "$f" = "./common_avx2_test" ] && ! grep -Fs avx2 /proc/cpuinfo ; then
		continue
	fi
	if [ "$f" = "./common_sse4_test" ] && ! grep -Fs sse4_1 /proc/cpuinfo ; then
		continue
	fi
	$f
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/gav1_decode
%attr(755,root,root) %{_libdir}/libgav1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgav1.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgav1.so
%{_includedir}/gav1
%{_pkgconfigdir}/libgav1.pc
%{_datadir}/cmake/libgav1-config.cmake

%files static
%defattr(644,root,root,755)
%{_libdir}/libgav1.a
