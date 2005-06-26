%bcond_with nhc			# build with nhc98, not ghc
Summary:	hmake is a compilation manager for Haskell programs
Summary(pl):	Program zarz±dzaj±cy kompilacj± programów w Haskellu
Name:		hmake
Version:	3.09
Release:	1
License:	Free
Group:		Development/Languages
Source0:	http://www.haskell.org/hmake/%{name}-%{version}.tar.gz
# Source0-md5:	72ac1fbca710dd8be5926600b119b4f4
Patch0:		%{name}-uname.patch
URL:		http://www.haskell.org/hmake/
BuildRequires:	ed
%{!?with_nhc:BuildRequires:	ghc}
BuildRequires:	gmp-devel
BuildRequires:	ncurses-devel
%{?with_nhc:BuildRequires:      nhc98}
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
hmake is a make(1) like command for compiling Haskell programs.
Dependencies are automatically extracted from the source files; there
is no need to construct or maintain a Makefile.

Hmake interactive, or hi for short, is an interpreter-like environment
that you can wrap over any common Haskell compiler to achieve an
interactive development style rather like Hugs.

%description -l pl
hmake jest poleceniem podobnym do make(1) przeznaczonym do
kompilowania programów w Haskellu. Zale¿no¶ci s± automatycznie
wyci±gane z plików ¼ród³owych; nie trzeba tworzyæ ani nadzorowaæ
Makefile.

Hmake interactive (w skrócie hi) jest interaktywnym, podobnym do
interpretera, ¶rodowiskiem, które mo¿na u¿ywaæ z dowolnym kompilatorem
Haskella aby dostaæ interaktywne ¶rodowisko podobne do Hugs.

%prep
%setup -q
%patch0 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}/%{name} \
	--mandir=%{_mandir}/man1 \
%{!?with_nhc:--buildwith=ghc} \
%{?with_nhc:--buildwith=nhc98} \
	--buildopts="-O"

%{__make} \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
./configure \
	--install \
	--libdir=$RPM_BUILD_ROOT%{_libdir}/%{name} \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--mandir=$RPM_BUILD_ROOT%{_mandir}/man1
%{__make} install

# correct hardcoded build-root path in some scripts
for f in $RPM_BUILD_ROOT%{_bindir}/{hi,hmake} ; do
ed -s $f <<EOF || :
,s|$RPM_BUILD_ROOT||g
wq
EOF
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT INSTALL README docs/hmake/*.*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/hmake
%dir %{_libdir}/hmake/*-Linux
%attr(755,root,root) %{_libdir}/hmake/*-Linux/HInteractive
%attr(755,root,root) %{_libdir}/hmake/*-Linux/MkProg
%attr(755,root,root) %{_libdir}/hmake/*-Linux/MkConfig
%attr(755,root,root) %{_libdir}/hmake/*-Linux/Older
%{_libdir}/hmake/*-Linux/config
%{_libdir}/hmake/*-Linux/hmakerc
%{_mandir}/*/*
