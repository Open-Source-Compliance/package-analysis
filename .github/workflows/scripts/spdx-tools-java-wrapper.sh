#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
# SPDX-FileCopyrightText: Helio Chissini de Castro <heliocastro@gmail.com>
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
    # Set default values that work to link to local files below.
    GITHUB_STEP_SUMMARY="${GITHUB_STEP_SUMMARY:-}"
    GITHUB_SERVER_URL="${GITHUB_SERVER_URL:-.}"
    GITHUB_REPOSITORY="${GITHUB_REPOSITORY:-.}"
    GITHUB_SHA="${GITHUB_SHA:-..}"

    if [[ -z "$GITHUB_STEP_SUMMARY" ]]; then
        GITHUB_STEP_SUMMARY="$(mktemp)"
        echo "Writing local job summary to '$GITHUB_STEP_SUMMARY'."
    fi

    # TODO: Limit this to only the files modified in a PR.
    find analysed-packages/ -iname '*.spdx' -print0 | \
        xargs -0 -P8 -I {} \
        bash -c "'$javabin' -jar '$jar' Verify {} || echo '* [{}]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$GITHUB_SHA/{})' >> '$GITHUB_STEP_SUMMARY'"

    if [[ -s "$GITHUB_STEP_SUMMARY" ]]; then
        local count=$(wc -l < "$GITHUB_STEP_SUMMARY")
        echo -e "### The following $count \`.spdx\` files are invalid :x: (see the job logs for details)\n$(cat $GITHUB_STEP_SUMMARY)" > "$GITHUB_STEP_SUMMARY"
        exit 1
    else
        echo "### All \`.spdx\` files are valid :heavy_check_mark:" > "$GITHUB_STEP_SUMMARY"
    fi
}

convert() {
    git config user.name github-actions
    git config user.email github-actions@github.com
    
    find analysed-packages/ -iname '*.spdx' -print0 |
        while IFS= read -r -d '' spdx; do
            json="${spdx/spdx/json}"
            yaml="${spdx/spdx/yaml}"
            if [ ! -f "$json" ]; then
                java -jar "$jar" Convert "$spdx" "$json"
                git add "$json"
            fi
            if [ ! -f "$yaml" ]; then
                java -jar "$jar" Convert "$spdx" "$yaml"
                git add "$yaml"
            fi
        done
    
    git commit -m "- Generated json and yaml formats"
    git push
}

"$@"
