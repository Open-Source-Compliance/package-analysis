#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
# SPDX-FileCopyrightText: Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: Jan Altenberg <jan.altenberg@osadl.org>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

if [ -z "${SPDX_TOOLS_VERSION}" ]; then
    echo "SPDX_TOOLS_VERSION is empty!"
    exit 1
fi

jar="$HOME/spdx-tools-java/tools-java-${SPDX_TOOLS_VERSION}-jar-with-dependencies.jar"

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

    local zip="tools-java-${SPDX_TOOLS_VERSION}.zip"
    local url="https://github.com/spdx/tools-java/releases/download/v${SPDX_TOOLS_VERSION}/${zip}"

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
