"""
Description
=====
Class RT is defined. RT is a class that is an instance of each attack technique.
"""
import os, subprocess, json, time, tempfile
import constant
from listener import Listener
from command import Command

class RT():
    """
    RT class is an instance of each attack.
    Information of attack and resources for performing attack are defined.
    """
    def __init__(self, name, cond, post, cmd):
        """
        Constructor

        :param name:The name of attack.
        :param cond:Precondition of attack.
        :param post:Postcondition of atack.
        :param cmd:Path of command file for this attack.
        """
        self.name = name
        self.cond = cond
        self.post = post
        self.cmd = cmd

    def __str__(self):
        msg = "name : " + self.name + "\n"
        msg += "command : " + self.cmd + "\n"
        msg += "preconditions :\n"
        msg += str(self.cond)
        msg += "postconditions :\n"
        if len(self.post) == 0:
            msg += "\tnone\n"
        else:
            for e in self.post:
                msg += "\t" + " ".join(e) + "\n"
        return msg

    def is_explorable(self, state):
        """
        Checks techniques are explorable based on the current state.
        Exploration is to collect possible attack scenarios.
        'ASSUMED' keyword is used to denotes a state can be updated with unknown values.
        Because, attack scenarios does not know the result of runtime.

        :param state:A given state to be checked.

        :return bool:True is explorable, otherwise False.
        """
        return self.cond.is_explorable(state)

    def mark_explored(self, state):
        """
        Update a state as if this attack is performed well.
        If a result of an attack scenario is not determined, "UNKNOWN" value is assigned.
        "UNKNOWN" value makes possible to connect attacks before attacks are performed actually.

        :param state:A given state to be marked.

        :return dictionary:A marked state.
        """
        for e in self.post:
            key = e[0]
            value = e[1]
            if e[1] == "UNKNOWN":
                state[key] = constant.STATE_VALUE_UNKNOWN
            else:
                state[key] = value
        return state

    def is_satisfied(self, state):
        """
        Checks this RT can be trigerred on a given state.

        :param state:A given state

        :return bool:True if an attack can be triggered, otherwise False.
        """
        return self.cond.is_satisfied(state)

    def run(self, interface, state):
        """
        Perform an attack.

        :param interface:Path for a file that is used as an interface between a red agent and attack scripts.
        Before attack script starts, if there is information that should be passed from a red agent,
        A red agent should store it in its state, and then store state to an interface file as a json format.
        Attack script loads the interface file as a json instance, and then use information inside it.
        Further, attack script can update the loaded state, and can store it into the same file.
        As a result, a red agent can get information by loading the interface file again after an attack is done.
        :param state:A given state to run an attack.
        """

        command = Command(self.cmd)

        state = command.run(state, interface)
        if "error" in state:
            print ("[E] " + state["error"])
            del state["error"]
            return state

        return state
