#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

version="1.1.4"
zip="tools-java-${version}.zip"
url="https://github.com/spdx/tools-java/releases/download/v${version}/${zip}"
jar="$HOME/spdx-tools-java/tools-java-${version}-jar-with-dependencies.jar"

bootstrap() {
    if [[ ! -f "$jar" ]]; then
        wget -q "$url"
        unzip "$zip" -d "$(dirname "$jar")" "$(basename "$jar")"
        rm "$zip"

        java -jar "$jar"
    fi
}

verify() {
    local tmpfile="$(mktemp)"
    find analysed-packages/ -iname '*.spdx' -print0 |
        while IFS= read -r -d '' spdx; do
            java -jar "$jar" Verify "$spdx" || {
                echo "$spdx" >> "$tmpfile"
            }
        done

    echo
    if [[ -s "$tmpfile" ]]; then
        echo "################################################################################"
        echo "The following .spdx files are not valid, see logs above:"
        echo
        cat "$tmpfile"
        echo "################################################################################"
        exit 1
    else
        echo "################################################################################"
        echo "all .spdx files are valid"
        echo "################################################################################"
    fi
}

"$@"
