Summary:	John the Ripper password cracker
Name:		john
Version:	1.9.0
Release:	1
License:	GPLv2+
Group:		Monitoring
Url:		https://www.openwall.com/john
Source0:	https://www.openwall.com/john/k/%{name}-%{version}-jumbo-1.tar.gz
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
%autosetup -p1 -n %{name}-%{version}-jumbo-1

%build
cd src
%configure
%make_build

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

