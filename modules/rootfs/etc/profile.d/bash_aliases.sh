#!/bin/sh

# detailed file and directory listing
alias ll='ls -alih --color=always'
alias ls='ls --color=always'
alias rm='trash -v'
alias cp='cp -i'
alias mv='mv -i'
alias edit='$(echo ${EDITOR})'

upgrade_all()
{
    paru_bin="$(command -v paru)"
    paru_args="-Syuu --needed --sudoloop"

    eval $paru_bin $paru_args
}
