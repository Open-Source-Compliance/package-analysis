#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
# SPDX-FileCopyrightText: Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

version="1.1.7"
jar="$HOME/spdx-tools-java/tools-java-${version}-jar-with-dependencies.jar"

spdx_tools() {
    local javabin
    if [[ -v "JAVA_HOME" && -x "$JAVA_HOME/bin/java" ]]; then
        javabin="$JAVA_HOME/bin/java"
    else
        javabin=java
    fi

    "$javabin" -jar "$jar" "$@"
}

bootstrap() {
    [[ -f "$jar" ]] && return

    local zip="tools-java-${version}.zip"
    local url="https://github.com/spdx/tools-java/releases/download/v${version}/${zip}"

    curl -LOs "$url"
    unzip "$zip" -d "$(dirname "$jar")" "$(basename "$jar")"
    rm "$zip"

    spdx_tools Version
}

if [[ "$1" == "bootstrap" ]]; then
    bootstrap
else
    spdx_tools "$@"
fi
