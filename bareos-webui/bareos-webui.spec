
Name:          bareos-webui
Version:       18.2.6
Release:       1%{?dist}
Summary:       Bareos Web User Interface

Group:         Productivity/Archiving/Backup
License:       AGPL-3.0+
URL:           http://www.bareos-webui.org/
Vendor:        The Bareos Team
Source:        bareos-Release-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
BuildArch:     noarch

%if 0%{?centos} || 0%{?rhel}
BuildRequires: cmake
BuildRequires: cmake3
%else
BuildRequires: cmake
%endif
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: bareos-common

# ZendFramework 2.4 says it required php >= 5.3.23.
# However, it works on SLES 11 with php 5.3.17
# while it does not work with php 5.3.3 (RHEL6).
Requires: php >= 5.3.17

Requires: php-bz2
Requires: php-ctype
Requires: php-curl
Requires: php-date
Requires: php-dom
Requires: php-fileinfo
Requires: php-filter
Requires: php-gettext
Requires: php-gd
Requires: php-hash
Requires: php-iconv
Requires: php-intl
Requires: php-json
Requires: php-libxml
Requires: php-mbstring
#Requires: php-mysql
Requires: php-openssl
Requires: php-pcre
#Requires: php-pdo
#Requires: php-pecl
#Requires: php-pgsql
Requires: php-reflection
Requires: php-session
Requires: php-simplexml
Requires: php-spl
Requires: php-xml
Requires: php-xmlreader
Requires: php-xmlwriter
Requires: php-zip

#define serverroot #(/usr/sbin/apxs2 -q datadir 2>/dev/null || /usr/sbin/apxs2 -q PREFIX)/htdocs/

%description
Bareos - Backup Archiving Recovery Open Sourced. \
Bareos is a set of computer programs that permit you (or the system \
administrator) to manage backup, recovery, and verification of computer \
data across a network of computers of different kinds. In technical terms, \
it is a network client/server based backup program. Bareos is relatively \
easy to use and efficient, while offering many advanced storage management \
features that make it easy to find and recover lost or damaged files. \
Bareos source code has been released under the AGPL version 3 license.

This package contains the webui (Bareos Web User Interface).

%prep -n bareos-Release-%{version}/webui
%setup -n bareos-Release-%{version}/webui

%build
%if 0%{?rhel} < 8
cmake3 . \
%else
cmake  . \
%endif
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DCMAKE_INSTALL_PREFIX:PATH=/usr \
  -DCMAKE_INSTALL_LIBDIR:PATH=/usr/lib \
  -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
  -DLIB_INSTALL_DIR:PATH=/usr/lib \
  -DSYSCONF_INSTALL_DIR:PATH=/etc \
  -DSHARE_INSTALL_PREFIX:PATH=/usr/share \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -Dsysconfdir=%{_sysconfdir} \
  -Dconfdir=%{_sysconfdir}/bareos \
  -Dwebuiconfdir=%{_sysconfdir}/bareos-webui \
  -DVERSION_STRING=%version

make

%install
make DESTDIR=%{buildroot} install

# With the introduction of config subdirectories (bareos-16.2)
# some config files have been renamed (or even splitted into multiple files).
# However, bareos is still able to work with the old config files,
# but rpm renames them to *.rpmsave.
# To keep the bareos working after updating to bareos-16.2,
# we implement a workaroung:
#   * post: if the old config exists, make a copy of it.
#   * (rpm exchanges files on disk)
#   * posttrans:
#       if the old config file don't exists but we have created a backup before,
#       restore the old config file.
#       Remove our backup, if it exists.
# This update helper should be removed wih bareos-17.x.

%define post_backup_file() \
if [ -f  %1 ]; then \
      cp -a %1 %1.rpmupdate.%{version}.keep; \
fi; \
%nil

%define posttrans_restore_file() \
if [ ! -e %1 -a -e %1.rpmupdate.%{version}.keep ]; then \
   mv %1.rpmupdate.%{version}.keep %1; \
fi; \
if [ -e %1.rpmupdate.%{version}.keep ]; then \
   rm %1.rpmupdate.%{version}.keep; \
fi; \
%nil

%post
%post_backup_file /etc/bareos/bareos-dir.d/webui-consoles.conf
%post_backup_file /etc/bareos/bareos-dir.d/webui-profiles.conf

%posttrans
%posttrans_restore_file /etc/bareos/bareos-dir.d/webui-consoles.conf
%posttrans_restore_file /etc/bareos/bareos-dir.d/webui-profiles.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%doc doc/README-TRANSLATION.md
%doc tests/selenium
%{_datadir}/%{name}/
%dir /etc/bareos-webui
%config(noreplace) /etc/bareos-webui/directors.ini
%config(noreplace) /etc/bareos-webui/configuration.ini
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/console/admin.conf.example
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/profile/webui-admin.conf

%changelog
* Sat May  4 2019 Paul Trunk <ptrunk@sysalpine.com> - 18.2.6-1
- Initial package
