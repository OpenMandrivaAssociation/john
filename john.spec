%define name    john
%define version 1.7.9
%define release 1

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    John the Ripper password cracker
License:    GPL
Group:      Monitoring
URL:        http://www.openwall.com/john
Source0:     http://www.openwall.com/john/g/%{name}-%{version}.tar.gz
#Patch0:     http://www.openwall.com/john/contrib/%{name}-%{version}-jumbo-6.tar.bz2
#Source:     http://www.openwall.com/john/contrib/%{name}-%{version}-jumbo-6.tar.bz2
Patch1:     john-1.7.8-fhs.patch
BuildRequires: openssl-devel

%description
John the Ripper is a fast password cracker, currently available for many
flavors of Unix (11 are officially supported, not counting different
architectures), DOS, Win32, and BeOS. Its primary purpose is to detect
weak Unix passwords, but a number of other hash types are supported as
well.

Build Options:
--define 'extra_cflags <cflags>'    Provide additional cflags

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .fhs
chmod 644 doc/*

%build
TARGET=""
%ifarch %ix86
    %ifarch i686
    TARGET=linux-x86-mmx
    %else
    TARGET=linux-x86-any
    %endif
%else
    %ifarch x86_64
    TARGET=linux-x86-64
    %endif
    %ifarch ppc
    TARGET=linux-ppc
    %endif
    %ifarch alpha
    TARGET=linux-alpha
    %endif
    %ifarch sparc
    TARGET=linux-sparc
    %endif
%endif

if test -z "$TARGET"; then
    TARGET=generic
    export TARGET
    echo "Please add the right TARGET to the spec file"
fi

cd src
%make $TARGET CFLAGS="-c -Wall %{optflags} %{?extra_cflags:%extra_cflags}"

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_datadir}/%{name} \
         %{buildroot}%{_sysconfdir}

install -m 755 run/{john,mailer} %{buildroot}%{_bindir}/
install -m 644 run/*.chr run/password.lst %{buildroot}%{_datadir}/%{name}/
install -m 644 run/john.conf %{buildroot}%{_sysconfdir}/

pushd %{buildroot}%{_bindir}
  ln -s john unafs
  ln -s john unique
  ln -s john unshadow
popd

%files
%doc doc/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_bindir}/*
%{_datadir}/%{name}





%changelog
* Fri Feb 24 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.7.9-1
+ Revision: 780102
- version update 1.7.9

* Tue Oct 18 2011 Leonardo Coelho <leonardoc@mandriva.org> 1.7.8-1
+ Revision: 705161
- bump new version

* Thu Jun 16 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.7-1
+ Revision: 685582
- new version
- switch to jumbo source tarball directly, instead of official version + patch

* Sat Jul 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.6-1mdv2011.0
+ Revision: 554503
- new version

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1.7.5-2mdv2010.1
+ Revision: 537328
- rebuild

* Sun Feb 28 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.5-1mdv2010.1
+ Revision: 512683
- new version

* Thu Jan 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.4.2-1mdv2010.1
+ Revision: 494749
- new version

* Sat Jan 02 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.4-1mdv2010.1
+ Revision: 485149
- new version

* Mon Sep 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.3.4-1mdv2010.0
+ Revision: 446466
- new version
- drop format error patch, merged upstream
- change patches order

* Mon Sep 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.3.1-3mdv2010.0
+ Revision: 439652
- jumbo patch (support for tens of additional hash types)

* Sun Sep 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.3.1-2mdv2010.0
+ Revision: 438689
- fix format errors

* Mon Aug 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.3.1-1mdv2009.0
+ Revision: 270893
- new version

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 1.7.2-6mdv2009.0
+ Revision: 247414
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Dec 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.2-4mdv2008.1
+ Revision: 136771
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

