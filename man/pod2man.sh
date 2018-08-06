#! /bin/bash

PRGNAME="spman"
MANSECTION="8"
PODFILENAME="${PRGNAME}.pod"
OUTPUT="${PRGNAME}.${MANSECTION}"

pod2man "${PODFILENAME}" > "${OUTPUT}"
sed -i "s/^\\.IX Title .*/\\.IX Title \"SPMAN 8\"/" "${OUTPUT}"
sed -i "s/^\\.TH.*/\\.TH \"SPMAN\" \"8\" \"$(date +%Y-%m-%d)\" \"System\" \
\"Linux User Manual\"/" "${OUTPUT}"
nroff -man "${OUTPUT}" | less
