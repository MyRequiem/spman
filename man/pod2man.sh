#! /bin/bash

PODFILENAME="$1"
OUTPUT="$(basename "${PODFILENAME}" .pod)".8

if [ -z "${PODFILENAME}" ]; then
    echo "Usage: $0 program_name.pod"
    exit 0
fi

if ! [ -e "${PODFILENAME}" ]; then
    echo "File '$1' not found"
    exit 1
fi


pod2man "${PODFILENAME}" > "${OUTPUT}"
sed -i 's/^\\.IX.*/\\.IX Title "SPMAN 8"/' "${OUTPUT}"
sed -i "s/^\\.TH.*/\\.TH \"SPMAN\" \"8\" \"$(date +%Y-%m-%d)\" \"System\" \
\"Linux User Manual\"/" "${OUTPUT}"
nroff -man "${OUTPUT}" | less
