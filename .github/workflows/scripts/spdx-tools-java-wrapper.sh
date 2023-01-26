#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

version="1.1.4"
zip="tools-java-${version}.zip"
url="https://github.com/spdx/tools-java/releases/download/v${version}/${zip}"
jar="$HOME/spdx-tools-java/tools-java-${version}-jar-with-dependencies.jar"

if [[ -n "$JAVA_HOME" && -x "$JAVA_HOME/bin/java" ]]; then
    javabin="$JAVA_HOME/bin/java"
else
    javabin=java
fi

bootstrap() {
    [[ -f "$jar" ]] && return

    curl -LOs "$url"
    unzip "$zip" -d "$(dirname "$jar")" "$(basename "$jar")"
    rm "$zip"

    "$javabin" -jar "$jar" Version
}

verify() {
    local tmpfile="$(mktemp)"
    find analysed-packages/ -iname '*.spdx' -print0 |
        while IFS= read -r -d '' spdx; do
            "$javabin" -jar "$jar" Verify "$spdx" || {
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
