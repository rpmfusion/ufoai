Name:		ufoai
Version:	2.2.1
Release:	4%{?dist}
Summary:	UFO: Alien Invasion

Group:		Amusements/Games
License:	GPLv2+
URL:		http://ufoai.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-source.tar.bz2
Source1:	%{name}.desktop
Source2:	%{name}-ded.desktop
Patch:		ufoai-2.2-libdir.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	desktop-file-utils curl-devel freealut-devel gettext
BuildRequires:	libjpeg-devel libogg-devel libpng-devel libvorbis-devel
BuildRequires:	libXxf86dga-devel libXxf86vm-devel SDL-devel SDL_mixer-devel
BuildRequires:	SDL_ttf-devel

Requires:	opengl-games-utils
Requires:	%{name}-data = %{version}


%package doc
Summary:	UFO: Alien Invasion user manual
Group:		Documentation
License:	GFDL
BuildRequires:	tetex-latex


%description
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment. You are in command of a small special unit which
has been founded to face the alien strike force. To be successful on
the long run, you will also have to have a research team study the
aliens and their technologies in order to learn as much as possible
about their technology, their goals and the aliens themselves.


%description doc
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment.

This package contains the user manual for the game.


%prep
%setup -q -n %{name}-%{version}-source
## we do not like "arch-dependent-file" in /usr/share
# change the target for the library
sed -i -e "s/base/./" build/game.mk
# allow to set the library path
%patch -p1


%build
%configure --disable-ufo2map --enable-release
make %{?_smp_mflags}
make %{?_smp_mflags} lang
# wrapper scripts - generated because we need arch dependent paths
cat > %{name}-wrapper.sh <<-EOF
#!/bin/sh

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK UFO:AI

exec ufo \\
	+set fs_libdir %{_libdir}/%{name} \\
	+set fs_basedir %{_datadir}/%{name} \\
	+set fs_i18ndir %{_datadir}/locale \\
	"\$@"
EOF

cat > ufoded-wrapper.sh <<-EOF
#!/bin/sh

exec ufoded \\
	+set fs_libdir %{_libdir}/%{name} \\
	+set fs_basedir %{_datadir}/%{name} \\
	+set fs_i18ndir %{_datadir}/locale \\
	"\$@"
EOF

# build documentation
cd src/docs/tex
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
install -D -m 0755 ufo %{buildroot}%{_bindir}/ufo
install -D -m 0755 ufoded %{buildroot}%{_bindir}
install -p -m 0755 %{name}-wrapper.sh %{buildroot}%{_bindir}
install -p -m 0755 ufoded-wrapper.sh %{buildroot}%{_bindir}
install -D -m 0755 game.so %{buildroot}%{_libdir}/%{name}/game.so
mkdir -p -m 0755 %{buildroot}%{_datadir}/locale
cp -pr base/i18n/* %{buildroot}%{_datadir}/locale/
mkdir -p -m 0755 %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
cp -p src/ports/linux/ufo.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
cp -p src/ports/linux/ufoded.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}-ded.png
desktop-file-install --vendor="fedora" \
	--dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --vendor="fedora" \
	--dir=%{buildroot}%{_datadir}/applications %{SOURCE2}
%find_lang %{name}
# install documentation
mkdir -p -m 0755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -pr README CONTRIBUTORS COPYING src/docs/tex/*.pdf \
	%{buildroot}%{_docdir}/%{name}-%{version}/


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
# we need to use full path so %doc does not the cleanup
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/CONTRIBUTORS
%doc %{_docdir}/%{name}-%{version}/COPYING
%{_bindir}/*
%{_libdir}/%{name}/
%{_datadir}/applications/*
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/32x32/
%{_datadir}/icons/hicolor/32x32/apps/


%files doc
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/*.pdf
%lang(en) %{_docdir}/%{name}-%{version}/ufo-manual_EN.pdf


%changelog
* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.2.1-4
- rebuild for new F11 features

* Thu Dec 11 2008 Karel Volny <kvolny@redhat.com> 2.2.1-3
- Fixed unowned directories (bug #225)

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.2.1-2
- rebuild

* Mon Jun 09 2008 Karel Volny <kvolny@redhat.com> 2.2.1-1
- Version bump
- Fixes Livna bug #1931
- Configure with --enable-release

* Tue Feb 26 2008 Karel Volny <kvolny@redhat.com> 2.2-5
- Added patch to allow setting fs_libdir, fixes Livna bug #1882

* Tue Feb 19 2008 Karel Volny <kvolny@redhat.com> 2.2-4
- Changed BuildRequires of the doc subpackage to tetex-latex instead of tetex

* Mon Feb 18 2008 Karel Volny <kvolny@redhat.com> 2.2-3
- Fixed BuildRequires to include SDL_mixer-devel

* Mon Feb 04 2008 Karel Volny <kvolny@redhat.com> 2.2-2
- Merged in ufoai-doc as a subpackage
- Added gtk-update-icon-cache to %%post and %%postun

* Tue Jan 22 2008 Karel Volny <kvolny@redhat.com> 2.2-1
- Version bump
- Added BuildRequires: curl-devel
- Changed language file handling
- Use bundled icons
- Added ufoded wrapper and menu entry

* Mon Jan 07 2008 Karel Volny <kvolny@redhat.com> 2.1.1-3
- Marked localisation files
- Some fixes according the comment #18 to bug #412001:
- Added BuildRequires: freealut-devel libXxf86vm-devel libXxf86dga-devel
- Improved .desktop file
- Added fix for mixed encoding within the file CONTRIBUTORS

* Thu Dec 06 2007 Karel Volny <kvolny@redhat.com> 2.1.1-2
- Split the game, data and additional music into separate packages
- Added wrapper script to use correct command line parameters and OpenGL Wrapper
- Added ufoai.desktop as a separate file

* Tue Dec 04 2007 Karel Volny <kvolny@redhat.com> 2.1.1-1
- Initial release for Fedora 8
