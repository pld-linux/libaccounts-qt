Summary:	Accounts management library for Qt 4 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 4
Name:		libaccounts-qt
Version:	1.15
Release:	2
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libaccounts-qt/tags?sort=updated_desc
Source0:	https://gitlab.com/accounts-sso/libaccounts-qt/repository/archive.tar.bz2?ref=VERSION_%{version}&fake_out=/%{name}-%{version}.tar.bz2
# Source0-md5:	e42c66030610d00f48a8c2c1ffc3ebe2
URL:		https://gitlab.com/accounts-sso/libaccounts-qt
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	doxygen
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaccounts-glib-devel
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is a library for managing accounts which can be used from
Qt applications. It is part of the accounts-sso project.

%description -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece Qt. Jest to część
projektu accounts-sso.

%package -n libaccounts-qt5
Summary:	Accounts management library for Qt 5 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 5
Group:		Libraries

%description -n libaccounts-qt5
This project is a library for managing accounts which can be used from
Qt 5 applications. It is part of the accounts-sso project.

%description -n libaccounts-qt5 -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece Qt 5. Jest to część
projektu accounts-sso.

%package -n libaccounts-qt5-devel
Summary:	Development files for libaccounts-qt5 library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libaccounts-qt5
Group:		Development/Libraries
Requires:	Qt5Core-devel >= 5
Requires:	libaccounts-qt5 = %{version}-%{release}

%description -n libaccounts-qt5-devel
Development files for libaccounts-qt5 library.

%description -n libaccounts-qt5-devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-qt5.

%package apidocs
Summary:	API documentation for libaccounts-qt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libaccounts-qt
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libaccounts-qt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libaccounts-qt.

%prep
%setup -q -n %{name}-VERSION_%{version}-5b272ae218ccdf1f67f4eed92e2cdbe21c56ceb8

%build
install -d build-qt5
cd build-qt5
qmake-qt5 ../accounts-qt.pro \
	BUILD_DIR=build-qt5 \
	LIBDIR=%{_libdir} \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-qt5 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt5.so.1.?

# test suite
%{__rm} $RPM_BUILD_ROOT%{_bindir}/accountstest
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/accounts-qt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libaccounts-qt5 -p /sbin/ldconfig
%postun	-n libaccounts-qt5 -p /sbin/ldconfig

%files -n libaccounts-qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccounts-qt5.so.1

%files -n libaccounts-qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt5.so
%{_includedir}/accounts-qt5
%{_pkgconfigdir}/accounts-qt5.pc
%{_libdir}/cmake/AccountsQt5

%files apidocs
%defattr(644,root,root,755)
%doc build-qt5/doc/html/*
