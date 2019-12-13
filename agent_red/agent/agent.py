#!/usr/bin/python
"""
Description
=====

The entry point of a red agent
"""

import os, subprocess, json, sys, signal, traceback
import constant
from attackdb import AttackDB
from rt import RT
from plan import Planner
from listener import Listener
from condition import Condition

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def main():
    """ The entry point of red agent """
    listener_port = constant.DEFAULT_LISTENER_PORT

    #TODO: Command line arguments should be handled elegantly.
    if len(sys.argv) > 1:
        listener_port = sys.argv[1]
    AttackDB().update()

    Listener().work(constant.DEFAULT_LISTENER_IP, int(listener_port))

    assumed_state = {
        constant.STATE_KEY_PROTOCOL : constant.STATE_VALUE_PROTOCOL_IP,
        constant.STATE_KEY_ADDRESS : constant.DEFAULT_TARGET_IP
    }

    goal = Condition()
    goal.add((constant.STATE_KEY_SHELL, constant.CONDITION_OPERATOR_EQUAL, constant.STATE_VALUE_SHELL_PERMANENT))
    goal.add((constant.STATE_KEY_PRIVILEGE, constant.CONDITION_OPERATOR_EQUAL, constant.STATE_VALUE_PRIVILEGE_ROOT))

    planner = Planner(assumed_state, goal)
    try:
        planner.make_plan()
        print (planner)
        planner.run()

    except Exception as e:
        traceback.print_exc()
        Listener().stop()
        raise e

    Listener().stop()
    sys.exit(0)

def signal_handler(sig, frame):
    """ Callback for handling signal(CTRL-C) to terminate threads """
    Listener().stop()
    sys.exit(0)
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
