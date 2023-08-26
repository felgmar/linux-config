#!/bin/sh
set -e

echo ":: Copying files..."
find rootfs/etc/ -type d -exec sudo cp -rv {} "/etc/" \;

