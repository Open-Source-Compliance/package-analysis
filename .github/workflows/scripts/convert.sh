#!/usr/bin/env bash

# SPDX-FileCopyrightText: Maximilian Huber <maximilian.huber@tngtech.com>
# SPDX-FileCopyrightText: Sebastian Schuberth <sschuberth@gmail.com>
# SPDX-FileCopyrightText: Helio Chissini de Castro <heliocastro@gmail.com>
# SPDX-FileCopyrightText: Jan Altenberg <jan.altenberg@osadl.org>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

convert_one() {
    local spdx="$1"
    local spdx_timestamp="$(git log -1 --pretty="format:%ci" "$spdx")"
    local temporary_spdx=""

    local json yaml rdf
    json="${spdx/-SPDX2TV/}.json"
    yaml="${spdx/-SPDX2TV/}.yaml"
    rdf="${spdx/-SPDX2TV/}.rdf.xml"

    if [[ "$spdx" == *.gz ]]; then
        >&2 echo "Unzipping $spdx"
        gunzip -fk $spdx
        spdx=${spdx%.*}
        temporary_spdx=$spdx
    fi

    for out in $json $yaml $rdf; do
        if [[ -f "$out" ]]; then
            local out_timestamp="$(git log -1 --pretty="format:%ci" "$out")"
            if [[ -f "$out.gz" ]]; then
                local out_timestamp="$(git log -1 --pretty="format:%ci" "$out.gz")"
            else
                local out_timestamp="$(git log -1 --pretty="format:%ci" "$out")"
            fi
            if [[ "$spdx_timestamp" -ot "$out_timestamp" ]]; then
                continue
            fi
            rm "$out"
        fi
        >&2 echo "Convert '$spdx' to '$out'"
        "${SCRIPT_DIR}/spdx-tools-java-wrapper.sh" Convert "$spdx" "$out" 1>&2;
        if test -n "$(find "$out" -size +50M)"
        then
            >&2 echo "$out exceeds threshold (50MB), compressing it..."
            gzip -f "$out"
            git add "${out}.gz"
        else
            git add "$out"
        fi
    done

    if [ -f "$temporary_spdx" ]; then
        >&2 echo "Deleting temporary file $temporary_spdx"
        rm $temporary_spdx
    fi
}

convert_many() {
    if [[ $# -eq 0 ]]; then
        >&2 echo "No .spdx files to convert"
        return 0
    fi

    for spdx in "$@"; do
        convert_one "$spdx"
    done
}

convert_all() {
    find analysed-packages/ -iname '*-SPDX2TV*.spdx' -print0 | \
        xargs -0 -P"$(nproc)" -I {} \
        bash -c "'$0' '{}'"
}

if [[ $# -eq 1 && "$1" == "all" ]]; then
    convert_all
else
    convert_many "$@"
fi
