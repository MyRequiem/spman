#! /bin/sh

VERSION=$(grep "self.prog_version = " src/maindata.py | cut -d \' -f 2)
INFILE="
    INSTALL
    README.md
    slackbuild/spman.info
"

for FILE in ${INFILE}; do
    sed "s/[0-9]\\.[0-9]\\.[0-9]/${VERSION}/g" "${FILE}" > "${FILE}_"
    rm -f "${FILE}"
    mv "${FILE}_" "${FILE}"
done
