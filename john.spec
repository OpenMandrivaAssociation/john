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



