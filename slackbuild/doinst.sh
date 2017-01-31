#!/usr/bin/env bash

config() {
    NEW="$1"
    OLD="$(dirname ${NEW})/$(basename ${NEW} .new)"
    if [ ! -r ${OLD} ]; then
        mv ${NEW} ${OLD}
    elif [ "$(cat ${OLD} | md5sum)" = "$(cat ${NEW} | md5sum)" ]; then
        rm ${NEW}
    fi
}

CONFIGS="\
    blacklist \
    repo-list \
    spman.conf \
"

for FILE in ${CONFIGS}; do
    config etc/spman/${FILE}.new
done
