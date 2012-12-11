%define modname htscanner
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A12_%{modname}.ini

Summary:	Htaccess support for PHP
Name:		php-%{modname}
Version:	1.0.1
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/htscanner
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
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


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2012.0
+ Revision: 795448
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 790152
- 1.0.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5
+ Revision: 761255
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4
+ Revision: 696431
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3
+ Revision: 695406
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2
+ Revision: 646650
- rebuilt for php-5.3.6

* Sat Feb 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 636134
- 1.0.0

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-0.0.r305647.4mdv2011.0
+ Revision: 629812
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-0.0.r305647.3mdv2011.0
+ Revision: 628133
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-0.0.r305647.2mdv2011.0
+ Revision: 600497
- rebuild

* Mon Nov 22 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-0.0.r305647.1mdv2011.0
+ Revision: 599641
- use a current svn snap

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-4mdv2011.0
+ Revision: 588835
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-3mdv2010.1
+ Revision: 514558
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-2mdv2010.1
+ Revision: 485386
- rebuilt for php-5.3.2RC1

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2010.1
+ Revision: 482770
- fix format string error (duh!)
- rebuilt against php-5.3.1
- rebuild
- 0.9.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-13mdv2009.1
+ Revision: 346502
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-12mdv2009.1
+ Revision: 341764
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-11mdv2009.1
+ Revision: 321796
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-10mdv2009.1
+ Revision: 310275
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-9mdv2009.0
+ Revision: 238402
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-8mdv2009.0
+ Revision: 200223
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-7mdv2008.1
+ Revision: 162228
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-6mdv2008.1
+ Revision: 107664
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-5mdv2008.0
+ Revision: 77548
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-4mdv2008.0
+ Revision: 39500
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-3mdv2008.0
+ Revision: 33811
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-2mdv2008.0
+ Revision: 21333
- rebuilt against new upstream version (5.2.2)

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8.1-1mdv2008.0
+ Revision: 14527
- 0.8.1


* Tue Feb 20 2007 Oden Eriksson <oeriksson@mandriva.com> 0.7.0-1mdv2007.0
+ Revision: 123012
- 0.7.0

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-2mdv2007.1
+ Revision: 117587
- rebuilt against new upstream version (5.2.1)

* Sun Jan 07 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.3-1mdv2007.1
+ Revision: 105366
- 0.6.3

* Mon Dec 18 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.2-1mdv2007.1
+ Revision: 98533
- 0.6.2
- bump release
- Import php-htscanner

* Wed Dec 13 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2007.1
- initial Mandriva package

