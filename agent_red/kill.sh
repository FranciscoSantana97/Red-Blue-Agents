#!/bin/bash
curpath=$(realpath $(dirname $0))

#(1) Kill Agent
agentpid=$(ps -ef | grep "python agent/agent.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$agentpid" ];
then
    kill -9 $agentpid
fi

serverpid=$(ps -ef | grep "rat/server_web.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$serverpid" ];
then
    kill -9 $serverpid
fi

sleeppid=$(ps -ef | grep "sleep.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$sleeppid" ];
then
    kill -9 $sleeppid
fi

../environment/kill.sh

#(2) Remove trashes
rm -f $curpath/temp_nfsop $curpath/temp.mvg $curpath/temp $curpath/malscript.sh $curpath/malware /etc/cron.d/malware /tmp/AAABBB
