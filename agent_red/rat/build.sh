#!/bin/bash

#So far it is not considered to cross compiling of RAT.
#Thus, only 32-bit system of Linux can be the target of this RAT.
#The followings are how to support to RAT for other systems.

#(1) Determines which host systems are supported in the framework.
#(2) Prepraring tool-chains for determined host systems.
#(3) Adding commands to build RATs for each determined host systems in here.
#(4) Run this script to build them.

#VARIABLES
curpath=$(dirname $(realpath $0))
input=rat.c
postfix=.c
output=${input%$postfix}

#Build scripts
gcc -o $curpath/$output $curpath/$input
