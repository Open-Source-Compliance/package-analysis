#!/usr/bin/env bash

# SPDX-FileCopyrightText: Jan Altenberg <jan.altenberg@osadl.org>
#
# SPDX-License-Identifier: CC0-1.0

set -euo pipefail

for spdx in "$@"; do
        if test -n "$(find "$spdx" -size +50M)"
        then
                >&2 echo "File size of $spdx exceeds 50MB limit"
                >&2 echo "Please compress with gzip"
                >&2 echo "If already compressed, try a higher compression rate"
                exit 1
        else
                >&2 echo "$spdx has valid size (<= 50MB)"
        fi
done

exit 0

