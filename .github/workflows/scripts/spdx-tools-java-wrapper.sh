#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

version="1.1.4"
jar="$HOME/spdx-tools-java/tools-java-${version}-jar-with-dependencies.jar"

spdx_tools() {
    local javabin
    if [[ -n "${JAVA_HOME+x}" && -x "$JAVA_HOME/bin/java" ]]; then
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

verify_one() {
    local spdx="$1"
    >&2 echo -e "\nVerify $spdx\n"

    # Set default values that work to link to local files below.
    GITHUB_SERVER_URL="${GITHUB_SERVER_URL:-.}"
    GITHUB_REPOSITORY="${GITHUB_REPOSITORY:-.}"
    GITHUB_SHA="${GITHUB_SHA:-..}"

    spdx_tools Verify "$spdx" 1>&2 || echo "* [$spdx]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$GITHUB_SHA/$spdx)"
}

check_github_step_summary() {
    if [[ -s "$GITHUB_STEP_SUMMARY" ]]; then
        local count
        count=$(wc -l < "$GITHUB_STEP_SUMMARY")
        echo -e "### The following $count \`.spdx\` files are invalid :x: (see the job logs for details)\n$(cat "$GITHUB_STEP_SUMMARY")" > "$GITHUB_STEP_SUMMARY"
        exit 1
    else
        echo "### All \`.spdx\` files are valid :heavy_check_mark:" > "$GITHUB_STEP_SUMMARY"
    fi
}

verify_many() {
    if [[ $# -eq 0 ]]; then
        >&2 echo "No .spdx files to verify"
        return 0
    fi

    if [[ -z "${GITHUB_STEP_SUMMARY+x}" ]]; then
        GITHUB_STEP_SUMMARY="$(mktemp)"
        echo "Writing local job summary to '$GITHUB_STEP_SUMMARY'."
    fi

    for spdx in "$@"; do
        verify_one "$spdx" >> "$GITHUB_STEP_SUMMARY"
    done

    check_github_step_summary
}

verify() {
    if [[ -z "${GITHUB_STEP_SUMMARY+x}" ]]; then
        GITHUB_STEP_SUMMARY="$(mktemp)"
        echo "Writing local job summary to '$GITHUB_STEP_SUMMARY'."
    fi

    find analysed-packages/ -iname '*.spdx' -print0 | \
        xargs -0 -P"$(nproc)" -I {} \
        bash -c "'$0' verify_one '{}'" >> "$GITHUB_STEP_SUMMARY"

    check_github_step_summary
}

"$@"
