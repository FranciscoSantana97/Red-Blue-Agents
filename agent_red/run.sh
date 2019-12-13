#!/bin/bash

#Variables
curpath=$(dirname $(realpath $0))

# Run environment
sudo $curpath/../environment/run.sh

# Run RAT
if [ ! -f $curpath/rat/rat ];
then
    $curpath/rat/build.sh
fi
python $curpath/rat/server_web.py 12000 &

sleep 1

# Run agent
sudo python agent/agent.py
