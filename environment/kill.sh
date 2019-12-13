#!/bin/bash

# Variables
curpath=$(dirname $(realpath $0))

if [ ! -z $(pgrep CVE-2016-3714) ];
then
    kill -9 $(pgrep CVE-2016-3714)
fi

if [ ! -z "$(pgrep php-fpm)" ];
then
    sudo service php7.0-fpm stop
fi

if [ ! -z "$(pgrep nginx)" ];
then
    sudo service nginx stop
fi

if [ ! -z "$(pgrep malware)" ];
then
    sudo kill -9 "$(pgrep malware)"
fi

if [ -f /etc/cron.d/malware ];
then
    sudo rm /etc/cron.d/malware
fi

if [ -f /tmp/AAABBB ];
then
    rm /tmp/AAABBB
fi
