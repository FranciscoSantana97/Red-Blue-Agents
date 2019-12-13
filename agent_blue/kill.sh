#! /bin/bash

# Kill agent
agentpid=$(ps -ef | grep "sudo python agent/agent_blue.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$agentpid" ]
then
	sudo kill -9 $agentpid
fi

# Kill snort
snortpid=$(ps -ef | grep "snort -A console -i ens33 -c /etc/snort/snort.conf" | grep -v grep | awk '{print $2}')
if [ ! -z "$snortpid" ]
then
	sudo kill -9 $snortpid
fi