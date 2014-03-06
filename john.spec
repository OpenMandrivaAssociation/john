Summary:	John the Ripper password cracker
Name:		john
Version:	1.8.0
Release:	2
License:	GPLv2+
Group:		Monitoring
Url:		http://www.openwall.com/john
Source0:	http://www.openwall.com/john/g/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(openssl)

%description
John the Ripper is a fast password cracker, currently available for many
flavors of Unix (11 are officially supported, not counting different
architectures), DOS, Win32, and BeOS. Its primary purpose is to detect
weak Unix passwords, but a number of other hash types are supported as
well.

%files
%doc doc/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_bindir}/*
%{_datadir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q
chmod 0644 doc/*

find . -perm 0600 | xargs chmod 0644

%build
TARGET=""
%ifarch %{ix86}
    %ifarch i686
    TARGET=linux-x86-mmx
    %else
    TARGET=linux-x86-any
    %endif
%else
    %ifarch x86_64
    TARGET=linux-x86-64
    %endif
%endif

if test -z "$TARGET"; then
    TARGET=generic
    export TARGET
    echo "Please add the right TARGET to the spec file"
fi

cd src
%make $TARGET CFLAGS="-c -Wall %{optflags} -DJOHN_SYSTEMWIDE=1" LDFLAGS="%{ldflags}"

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

pushd %{buildroot}%{_datadir}/%{name}
    ln -s %{_sysconfdir}/john.conf john.ini
popd

