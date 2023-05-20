Summary:	John the Ripper password cracker
Name:		john
Version:	1.9.0
Release:	3
License:	GPLv2+
Group:		Monitoring
Url:		https://www.openwall.com/john
Source0:	https://www.openwall.com/john/k/%{name}-%{version}-jumbo-1.tar.gz
# (upstream) https://github.com/openwall/john/issues/4604
Patch0:		john-1.9.0-build_with_gcc11.patch
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

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

#%{__perl} -pi.orig -e 's|^(\#define CFG_FULL_NAME)\s.+$|$1 "%{_sysconfdir}/%{name}.conf"|' src/params.h
sed -i -e 's|^(\#define CFG_FULL_NAME)\s.+$|$1 "%{_sysconfdir}/%{name}.conf"|' src/params.h

%build
# WARNING - john makefile is defining -c on the level of CFLAGS and not the compile lines
# when overriding the Makefile we need to keep this logic
ORIGCPU=$(echo "$CFLAGS" | grep -o -E -e '-m(sse2|avx|avx2|avx512|avx512f|xop)( |$)' | tr -d '\n' )
CFLAGS=$(echo "$CFLAGS" | sed -E 's/-m(sse2|avx|avx2|avx512|avx512f|xop)( |$)//;' )
#export CFLAGS="$CFLAGS -c -DJOHN_SYSTEMWIDE=1"
 
# ASFLAGS needs info about libraries same as LDFLAGS, but needs -c for compilation only
export ASFLAGS="-c $LDFLAGS"
 
# By default build with "make generic"

# ASFLAGS needs info about libraries same as LDFLAGS, but needs -c for compilation only
export ASFLAGS="-c $LDFLAGS"

ARCH_CHAIN="generic"
#global with_fallback 0
	
%ifarch x86_64
ARCH_CHAIN="linux-gnu linux-x86-64 linux-x86-64-avx linux-x86-64-xop linux-x86-64-avx2"
#global with_fallback 1
%endif

# Compile the fallback binary
#ARCH_FIRST=$( echo "${ARCH_CHAIN}" | cut -d ' ' -f 1 )
 
# WARNING: original LDFLAGS in Makefile contain -s to strip the binaries
# We need to override that
	
pushd src
%configure 
%make_build \
	"linux-x86-64-avx2" \
	CFLAGS="%{optflags} `echo "$CFLAGS" | sed -E 's/-m(sse2|avx|avx2|avx512|avx512f|xop)( |$)//;' )`  -Wall -c -DJOHN_SYSTEMWIDE=1" \
	LDFLAGS="%{ldflags}" \
	ASFLAGS="${ASFLAGS}"
	%nil
#make -C src "${ARCH_FIRST}" CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" ASFLAGS="${ASFLAGS}"
popd

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

