#!/bin/bash

# Variables
curpath=$(dirname $(realpath $0))

if [ -z $(pgrep CVE-2016-3714) ];
then
    $curpath/CVE-2016-3714/daemon/CVE-2016-3714 > /dev/null 2>&1 &
    $curpath/CVE-2015-5958/build.sh > /dev/null 2>&1 &
fi
