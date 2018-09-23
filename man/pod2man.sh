#! /bin/bash

PRGNAME="spman"
MANSECTION="8"

UPPERPPRGNAME=$(echo ${PRGNAME} | tr "[:lower:]" "[:upper:]")
PODFILENAME="${PRGNAME}.pod"
OUTPUT="${PRGNAME}.${MANSECTION}"

pod2man "${PODFILENAME}" > "${OUTPUT}"
sed -i "s/^\\.IX Title .*/\\.IX Title \"${UPPERPPRGNAME} ${MANSECTION}\"/" \
    "${OUTPUT}"
sed -i "s/^\\.TH.*/\\.TH \"${UPPERPPRGNAME}\" \"${MANSECTION}\" \
\"$(date +%Y-%m-%d)\" \"System\" \"Linux User Manual\"/" "${OUTPUT}"
nroff -man "${OUTPUT}" | less
