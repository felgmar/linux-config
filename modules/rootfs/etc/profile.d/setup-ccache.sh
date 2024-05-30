#!/bin/sh

if test "$(command -v ccache)"
then
    ccache --max-size 50G && ccache -o compression=true
else
    echo "error: cache was not found and thus compiling will be slower"
fi

