#!/bin/sh

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK UFO:AI

exec ufo \
	+set fs_i18ndir /usr/share/locale \
	"\$@"
