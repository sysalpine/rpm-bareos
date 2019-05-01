%define name libdroplet
%define release 1
%define version 1

# do not optimize during compile for debugging
%define noopt 1


Summary: Scality Droplet library
License: BSD
Name: %{name}
Version: 3.0.git.1510141874.bc2a9a0
Release: 2%{?dist}
Source: %{name}-%{version}.tar.bz2
Group: Development/Tools
BuildRequires: libxml2-devel
%if 0%{?fedora}
BuildRequires: pkgconf-pkg-config
%else
BuildRequires: pkgconfig(json)
%endif

BuildRequires: automake autoconf libtool check-devel openssl-devel bison libattr-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot



%description
Library to help the transition to object based cloud storage by providing a
structured API to simplify application developers job and address key user
concerns.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Scality Droplet library
Requires: libdroplet = %{version}-%{release}
Requires: libxml2-devel

%description devel
Header files needed to develop programs that link against the Droplet library.

%prep
%setup -q
#%%patch1 -p1

aclocal -I m4
autoreconf -i -f

%build

%if %{noopt}
export CFLAGS="-g"
export CXXFLAGS="-g"
export GCJFLAGS="-g"
%endif

%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
/sbin/ldconfig -N -n %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libdroplet.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/droplet.h
%{_includedir}/dropletp.h
%{_includedir}/droplet
%{_libdir}/libdroplet.so
%{_libdir}/libdroplet.a
%{_libdir}/libdroplet.la
%{_libdir}/pkgconfig/droplet-3.0.pc
