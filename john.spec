%global optflags %{optflags} -fcommon

Summary:	John the Ripper password cracker
Name:		john
Version:	1.9.0
Release:	5
License:	GPLv2+
Group:		Monitoring
Url:		https://www.openwall.com/john
Source0:	https://www.openwall.com/john/k/%{name}-%{version}-jumbo-1.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

%patchlist
# (upstream) https://github.com/openwall/john/issues/4604
john-1.9.0-build_with_gcc11.patch
john-opencl.patch

%description
John the Ripper is a fast password cracker, currently available for many
flavors of Unix (11 are officially supported, not counting different
architectures), DOS, Win32, and BeOS. Its primary purpose is to detect
weak Unix passwords, but a number of other hash types are supported as
well.

%files
%doc ../doc/*
%{_bindir}/*
%{_datadir}/%{name}

#----------------------------------------------------------------------------
%prep
%autosetup -p2 -n %{name}-%{version}-jumbo-1/src

%conf
%configure

%build
%make_build

%install
# As of 1.9.0-jumbo-1, "make install" isn't implemented
mkdir -p %{buildroot}%{_bindir} \
       %{buildroot}%{_datadir}/%{name}/rules \
       %{buildroot}%{_sysconfdir}

install -m 755 ../run/{john,mailer} %{buildroot}%{_bindir}/
install -m 644 ../run/*.chr ../run/password.lst %{buildroot}%{_datadir}/%{name}/
install -m 644 ../run/*.conf %{buildroot}%{_datadir}/%{name}/
install -m 644 ../run/rules/* %{buildroot}%{_datadir}/%{name}/rules/

pushd %{buildroot}%{_bindir}
    ln -s john unafs
    ln -s john unique
    ln -s john unshadow
popd
