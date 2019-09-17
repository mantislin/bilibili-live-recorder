#!/bin/sh

pushd "$(dirname ${0})" >/dev/null

IFS=$'\n'

while true; do
    echo ">>>> =============================="

    echo ">>>> python3 run.py $@"
    python3 run.py $@

    secDelay="1"
    echo ">>>> sleep ${secDelay}"
    sleep ${secDelay}
done

popd >/dev/null
