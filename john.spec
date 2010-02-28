%define name    john
%define version 1.7.5
%define release %mkrel 1

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    John the Ripper password cracker
License:    GPL
Group:      Monitoring
URL:        http://www.openwall.com/john
Source:     http://www.openwall.com/john/g/%{name}-%{version}.tar.bz2
Patch0:     http://www.openwall.com/john/contrib/%{name}-%{version}-jumbo-1.diff.gz
Patch1:     john-1.7.3.4-fhs.patch
BuildRequires: openssl-devel
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
John the Ripper is a fast password cracker, currently available for many
flavors of Unix (11 are officially supported, not counting different
architectures), DOS, Win32, and BeOS. Its primary purpose is to detect
weak Unix passwords, but a number of other hash types are supported as
well.

Build Options:
--define 'extra_cflags <cflags>'    Provide additional cflags

%prep
%setup -q
%patch0 -p1 -b .jumbo
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
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_bindir}/*
%{_datadir}/%{name}



