
# _with_nhc	- build with nhc98, not ghc

Summary:	hmake is a compilation manager for Haskell programs.
Name:		hmake
Version:	2.03
Release:	1
Copyright:	Freely available
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
URL:		http://www.cs.york.ac.uk/fp/%{name}/
Source0:	ftp://ftp.cs.york.ac.uk/pub/haskell/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-ghc.patch
%{!?_with_nhc:BuildRequires:	ghc}
%{?_with_nhc:BuildRequires:	nhc98}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
hmake is a make(1) like command for compiling Haskell programs.
Dependencies are automatically extracted from the source files; there
is no need to construct or maintain a Makefile.

Hmake interactive, or hi for short, is an interpreter-like environment
that you can wrap over any common Haskell compiler to achieve an
interactive development style rather like Hugs.

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

%{__make} OPT="$RPM_OPT_FLAGS"

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
%{_libdir}/hmake
%{_mandir}/*/*
