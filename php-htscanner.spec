%define modname htscanner
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A12_%{modname}.ini

Summary:	Htaccess support for PHP
Name:		php-%{modname}
Version:	0.8.1
Release:	%mkrel 9
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/htscanner
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Allow one to use htaccess-like file to configure PHP per directory, just like
apache's htaccess. It is especially useful with fastcgi. This package was
originally developed by Bart Vanbrabant. Old versions are available
from: http://files.zoeloelip.be/htscanner

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

; The configuration file htscanner needs to scan for php_* directives
config_file=".htaccess"

; The fallback docroot when htscanner can't determine the current docroot
default_docroot="/"
default.ttl=300

; Stop when an error occured in RINIT (no document root, cannot get path_translated,...)
stop_on_error = 0
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS README package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
