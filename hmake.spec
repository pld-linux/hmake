
# _with_nhc	- build with nhc98, not ghc

Summary:	hmake is a compilation manager for Haskell programs
Summary(pl):	Program zarz±dzaj±cy kompilacj± programów w Haskellu
Name:		hmake
Version:	2.03
Release:	3
License:	Freely available
Group:		Development/Languages
Source0:	ftp://ftp.cs.york.ac.uk/pub/haskell/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-ghc.patch
URL:		http://www.cs.york.ac.uk/fp/%{name}/
%{!?_with_nhc:BuildRequires:	ghc}
%{?_with_nhc:BuildRequires:	nhc98}
BuildRequires:	ed
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
%patch -p1

%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}/man1 \
%{!?_with_nhc:--buildwith=ghc} \
%{?_with_nhc:--buildwith=nhc98} \
	--buildopts="-O"

%{__make} OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
./configure \
    --install \
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

gzip -9nf COPYRIGHT INSTALL README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/hmake/*.*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/hmake
%attr(755,root,root) %{_libdir}/hmake/pld-Linux/HInteractive
%attr(755,root,root) %{_libdir}/hmake/pld-Linux/MkProg
%attr(755,root,root) %{_libdir}/hmake/pld-Linux/Older
%attr(755,root,root) %{_libdir}/hmake/pld-Linux/hmake.config
%{_libdir}/hmake/pld-Linux/config
%{_mandir}/*/*
