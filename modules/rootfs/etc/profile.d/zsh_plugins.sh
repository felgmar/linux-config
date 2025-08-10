#!/bin/sh

ZSH_AUTOSUGGESTIONS="/usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
ZSH_SYNTAX_HIGHLIGHTING="/usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"

if test -f "${ZSH_AUTOSUGGESTIONS}"
then
    source "${ZSH_AUTOSUGGESTIONS}"
fi

if test -f "${ZSH_SYNTAX_HIGHLIGHTING}"
then
    source "${ZSH_SYNTAX_HIGHLIGHTING}"
fi
