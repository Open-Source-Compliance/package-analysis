#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
# SPDX-FileCopyrightText: Helio Chissini de Castro <heliocastro@gmail.com>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GITHUB_STEP_SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

verify_one() {
    local spdx="$1"
    local temporary_spdx=""

    local verificationCacheFile=".verifications/${spdx}.verified"

    if sha1sum -c "$verificationCacheFile" &>/dev/null; then
        return
    fi

    if [[ "$spdx" == *.gz ]]; then
        >&2 echo "Unzipping $spdx"
        gunzip -fk $spdx
        spdx=${spdx%.*}
        temporary_spdx=${spdx}
    fi

    >&2 echo "Verify $spdx"

    if "${SCRIPT_DIR}/spdx-tools-java-wrapper.sh" Verify "$spdx" 1>&2; then
        mkdir -p "$(dirname "$verificationCacheFile")"
        sha1sum "$spdx" > "$verificationCacheFile"
    else
        # Set default values that work to link to local files below.
        GITHUB_SERVER_URL="${GITHUB_SERVER_URL:-.}"
        GITHUB_REPOSITORY="${GITHUB_REPOSITORY:-.}"
        GITHUB_SHA="${GITHUB_SHA:-..}"

        echo "* [$spdx]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$GITHUB_SHA/$spdx)"
    fi

    if [ -f "${temporary_spdx}" ]; then
        >&2 echo "Deleting temporary file ${temporary_spdx}"
	rm ${temporary_spdx}
    fi
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

    if [[ -v "GITHUB_STEP_SUMMARY" ]]; then
        GITHUB_STEP_SUMMARY="$(mktemp)"
        echo "Writing local job summary to '$GITHUB_STEP_SUMMARY'."
    fi

    for spdx in "$@"; do
        verify_one "$spdx" >> "$GITHUB_STEP_SUMMARY"
    done

    check_github_step_summary
}

verify_all() {
    if [[ -z "${GITHUB_STEP_SUMMARY+x}" ]]; then
        GITHUB_STEP_SUMMARY="$(mktemp)"
        echo "Writing local job summary to '$GITHUB_STEP_SUMMARY'."
    fi

    find analysed-packages/ -iname '*.spdx' -print0 | \
        xargs -0 -P"$(nproc)" -I {} \
        bash -c "'$0' one '{}'" >> "$GITHUB_STEP_SUMMARY"

    check_github_step_summary
}

if [[ $# -eq 1 && "$1" == "all" ]]; then
    verify_all
elif [[ $# -eq 2 && "$1" == "one" ]]; then
    shift
    verify_one "$1"
else
    verify_many "$@"
fi

