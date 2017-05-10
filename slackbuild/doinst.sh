#!/bin/bash

CONFIGS="\
    blacklist \
    repo-list \
    spman.conf \
"

for CONFIG in ${CONFIGS}; do
    OLD="/etc/spman/${CONFIG}"
    NEW="${OLD}.new"
    if ! [ -r "${OLD}" ]; then
        mv "${NEW}" "${OLD}"
    else
        MD5OLD=$(md5sum "${OLD}" | cut -d " " -f 1)
        MD5NEW=$(md5sum "${NEW}" | cut -d " " -f 1)
        if [[ "x${MD5OLD}" == "x${MD5NEW}" ]]; then
            rm "${NEW}"
        fi
    fi
done
