#!/bin/sh

zsh_plugins="/usr/share/zsh/plugins"

for plugin in ${zsh_plugins}/*/*.plugin.zsh
do
    source "${plugin}"
    if test $? -ne 0
    then
        echo "[!] zsh: failed to load plugin $(basename ${plugin})"
	return 1
    fi
done

