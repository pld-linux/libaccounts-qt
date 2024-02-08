# Conditional build:
%bcond_without	qt5	# build qt5 version
%bcond_without	qt6	# build qt6 version
Summary:	Accounts management library for Qt 4 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 4
Name:		libaccounts-qt
Version:	1.16
Release:	2
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://gitlab.com/accounts-sso/libaccounts-qt/tags?sort=updated_desc
Source0:	https://gitlab.com/accounts-sso/libaccounts-qt/-/archive/VERSION_%{version}/libaccounts-qt-VERSION_%{version}.tar.bz2
# Source0-md5:	36fd9d6b6fd5582bf6c503bfd3827a62
URL:		https://gitlab.com/accounts-sso/libaccounts-qt
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Test-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= 5
BuildRequires:	Qt6Test-devel >= 5
BuildRequires:	Qt6Xml-devel >= 5
BuildRequires:	qt6-build >= 5
BuildRequires:	qt6-qmake >= 5
%endif
BuildRequires:	doxygen
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaccounts-glib-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
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

%package -n libaccounts-qt6
Summary:	Accounts management library for Qt 6 applications
Summary(pl.UTF-8):	Biblioteka do zarządzania kontami dla aplikacji opartych na bibliotece Qt 6
Group:		Libraries

%description -n libaccounts-qt6
This project is a library for managing accounts which can be used from
Qt 6 applications. It is part of the accounts-sso project.

%description -n libaccounts-qt6 -l pl.UTF-8
Ten projekt to biblioteka do zarządzania kontami, z której można
korzystać w aplikacjach opartych na bibliotece Qt 6. Jest to część
projektu accounts-sso.

%package -n libaccounts-qt6-devel
Summary:	Development files for libaccounts-qt6 library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libaccounts-qt6
Group:		Development/Libraries
Requires:	Qt6Core-devel >= 5
Requires:	libaccounts-qt6 = %{version}-%{release}

%description -n libaccounts-qt6-devel
Development files for libaccounts-qt6 library.

%description -n libaccounts-qt6-devel -l pl.UTF-8
Pliki programistyczne biblioteki libaccounts-qt6.

%package apidocs
Summary:	API documentation for libaccounts-qt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libaccounts-qt
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libaccounts-qt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libaccounts-qt.

%prep
%setup -q -n %{name}-VERSION_%{version}
echo 'INCLUDEPATH += ..' >>Accounts/Accounts.pro
# tests are currently broken for qt6 (qmake not
# knowing "testlib")
sed -i -e 's, tests,,' *.pro

mkdir -p qt5
mv $(ls |grep -v qt5) qt5/
cp -a qt5 qt6
find qt6 -name "*5*" |while read i; do
    mv $i ${i/5/6}
done
find qt6 -type f |xargs sed -i -e 's,Qt5,Qt6,g;s,qt5,qt6,g'

%build
%if %{with qt5}
cd qt5
qmake-qt5 accounts-qt.pro \
	LIBDIR=%{_libdir} \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
%{__make}
cd ..
%endif
%if %{with qt6}
cd qt6
qmake-qt6 accounts-qt.pro \
	LIBDIR=%{_libdir} \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%{__make} -C qt5 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif
%if %{with qt6}
%{__make} -C qt6 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlink
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/libaccounts-qt?.so.1.?

# test suite
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/accountstest
# packaged as %doc
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/accounts-qt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libaccounts-qt5 -p /sbin/ldconfig
%postun	-n libaccounts-qt5 -p /sbin/ldconfig
%post	-n libaccounts-qt6 -p /sbin/ldconfig
%postun	-n libaccounts-qt6 -p /sbin/ldconfig

%if %{with qt5}
%files -n libaccounts-qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt5.so.*.*
%ghost %{_libdir}/libaccounts-qt5.so.1

%files -n libaccounts-qt5-devel
%defattr(644,root,root,755)
%{_libdir}/libaccounts-qt5.so
%{_includedir}/accounts-qt5
%{_libdir}/cmake/AccountsQt5
%endif

%if %{with qt6}
%files -n libaccounts-qt6
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccounts-qt6.so.*.*
%ghost %{_libdir}/libaccounts-qt6.so.1

%files -n libaccounts-qt6-devel
%defattr(644,root,root,755)
%{_libdir}/libaccounts-qt6.so
%{_includedir}/accounts-qt6
%{_libdir}/cmake/AccountsQt6
%endif

%files apidocs
%defattr(644,root,root,755)
%doc qt5/doc/html/*
