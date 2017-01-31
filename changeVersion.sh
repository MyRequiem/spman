#! /bin/sh

VERSION=$(grep "self.prog_version = " src/maindata.py | cut -d \' -f 2)
TMP=tmp
INFILE="
    INSTALL
    README.md
"

for FILE in ${INFILE}; do
    sed "s/[0-9]\.[0-9]\.[0-9]/${VERSION}/g" "${FILE}" > ${TMP}
    rm -f "${FILE}"
    mv ${TMP} "${FILE}"
done
