#!/bin/sh

popdDepth=0
if [[ "${PWD}" == "${HOME}" ]]; then
    pushd "$(dirname ${0})" >/dev/null
    popdDepth=$((${popdDepth}+1))
fi
IFS=$'\n'

while true; do
    echo ">>>> =============================="

    echo ">>>> python3 run.py $@"
    python3 run.py $@

    secDelay="1"
    echo ">>>> sleep ${secDelay}"
    sleep ${secDelay}
done

for (( i=0; i<${popdDepth}; i++ )); do
    popd >/dev/null
done
