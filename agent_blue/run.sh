#! /bin/bash

# Run agent
# TODO : install + run option 
if [ "$#" -eq 1 ]
then
	if [ "$1" = "-Im" ]
	then
		sudo sh agent/install/install_osqueryd.sh
	elif [ "$1" = "-Is" ]
	then
		sudo sh agent/install/install_snort.sh
	else
		echo "Wrong Argument"
	fi

elif [ "$#" -eq 2 ]
then
	if [ "$1" = "-M" ]
	then
		sudo python agent/agent_blue.py -M $2
	elif [ "$1" = "-B" ]
	then
		sudo python agent/agent_blue.py -B $2
	elif [ "$1" = "-L" ]
	then
		sudo python agent/agent_blue.py -L $2
	elif [ "$1" = "-C" ]
	then
		sudo python agent/agent_blue.py -C $2
	elif [ "$1" = "-F" ]
	then	
		sudo python agent/agent_blue.py -F $2
	else
		echo "Wrong Argument"
	fi

elif [ "$#" -eq 4 ]
then
	if [ "$1" = "-S" ] && [ "$3" = "-I" ]
	then
		sudo python agent/agent_blue.py -S $2 -I $4
	elif [ "$1" = "-F" ] && [ "$3" = "-M" ]
	then
		sudo python agent/agent_blue.py -F $2 -M $4
	elif [ "$1" = "-M" ] && [ "$3" = "-T" ]
	then
		sudo python agent/agent_blue.py -M $2 -T $4

	else
		echo "Wrong Argument"
	fi

elif [ "$#" -eq 6 ]
then
	if [ "$1" = "-S" ] && [ "$3" = "-I" ] && [ "$5" = "-M" ]
	then
		sudo python agent/agent_blue.py -S $2 -I $4 -M $6
	elif [ "$1" = "-F" ] && [ "$3" = "-M" ] && [ "$5" = "-T" ]
	then
		sudo python agent/agent_blue.py -F $2 -M $4 -T $6
	elif [ "$1" = "-B" ] && [ "$3" = "-L" ] && [ "$5" = "-C" ]
	then
		sudo python agent/agent_blue.py -B $2 -L $4 -C $6
	else
		echo "Wrong Argument"
	fi

elif [ "$#" -eq 8 ]
then
	if [ "$1" = "-S" ] && [ "$3" = "-I" ] && [ "$5" = "-M" ] && [ "$7" = "-T" ]
	then
		sudo python agent/agent_blue.py -S $2 -I $4 -M $6 -T $8
	fi
else
	echo "Wrong Argument"
fi
