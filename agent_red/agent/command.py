"""
Description
=====

Managing instances of a set of commands which are specified externally.
"""

import json, subprocess, shlex, os
from listener import Listener

class Command():
    """
    Managing a set of commands which are stored in an external command file.
    The format of command file is strongly linked to code of this class.
    Thus, only this class will be affected if the format changes.
    """
    def __init__(self, src):
        """
        Act as a constructor for the class.
        An instance will hold an instance of json after parsing file that passed through the parameter.

        :param src: a path of an external command file.
        """
        with open(src, "r") as f:
            self.raw = json.loads(f.read())
            self.idx = 0

    def __str__(self):
        return str(self.raw)

    def __is_done(self):
        """
        Checks whether all commands are performed.
        This instance has a set of commands in a queue.
        Each command is perfomed only once through the method \"__run_once\".
        After calling \"__run_once\", performed command is pulled out from the queue in this instance.
        Thus, before calling \"__run_once\", it is recommended to check whether any command is left in the queue.

        :return: bool True if there is command to be perfomed in the queue, otherwise False.
        """
        if self.idx < len(self.raw):
            return False
        else:
            return True        

    def __is_local(self):
        """
        Checks whether the current command is performed locally.
        There are two types of a command: local, remote.

        :return: bool True if the command should be performed locally, otherwise False.
        """
        if self.raw[self.idx]["TYPE"] == "LOCAL":
            return True
        else:
            return False

    def __get_command_type(self):
        """
        Provides a type of a command.
        There are two types of command: FILE, CMD.
        FILE denotes a command is a path of python script, thus it should be executed with python.
        CMD denotes a command is a bash command, thus it should be executed with bash.

        :return: string FILE or CMD.
        """
        return self.raw[self.idx]["CMD_TYPE"]

    def __get_command(self, state):
        """
        Providing command.

        :return: string python path if a command type is FILE, otherwise bash command.
        """
        command = self.raw[self.idx]["CMD"]
        try:
            rep = self.raw[self.idx]["REPLACE"]
            command = command.replace(rep[0], state[rep[1]])
        except KeyError:
            pass
            
        return command

    def __get_recv(self):
        """
        Providing a state key to store a result of a command.

        :return: string state key.
        """
        try:
            return self.raw[self.idx]["RECV"]
        except KeyError:
            return "NONE"

    def __run_once(self, state, interface):
        """
        Perform command.

        :param: state State
        :param: interface A file path used an interface between an agent and an external attack script.

        :return: Dict state
        """
        response = None

        with open(interface, "w") as f:
            json.dump(state, f)

        if self.__is_local():
            state = self.__run_local(state, interface)
        else:
            state = self.__run_remote(state)

        self.idx += 1
        return state

    def __run_local(self, state, interface):
        """
        Perform command.
        This is for executing command on local machine, which means it will not interact with Listener.

        :param: state State
        :param: interface A file path used as an interface between an agent and an external attack script.

        :return: Dict state
        """
        command = self.__get_command(state)
        args = shlex.split(command)
        args.append(interface)

        with open(os.devnull, "wb") as err:
            subprocess.Popen(args, stdout = err, stderr = err).communicate()

        with open(interface, "r") as f:
            state = json.load(f)

        if self.__get_recv() == "interface":
            pass
        elif self.__get_recv() == "shell":
            shell_state = Listener().get_state(state["address"])
            if shell_state != None:
                state["shell"] = shell_state
        else:
            raise RuntimeError("NOT IMPLEMENTED")

        return state

    def __run_remote(self, state):
        """
        Perform command(private method related to \"run\" method)
        This is for executing command on remote machine, which means it will interact with Listener.

        :param: state State

        :return: Dict state
        """
        interface = state["address"]

        if self.__get_command_type() == "FILE":
            raise RuntimeError("NOT IMPLEMENTED")
        
        if self.__get_recv() == "NONE":
            Listener().send_only(interface, self.__get_command(state))
        elif self.__get_recv() == "shell":
            Listener().send_only(interface, self.__get_command(state))
            Listener().update_state_as_address(interface)
            state["shell"] = Listener().get_state(interface)
        else:
            print ("command : " + self.__get_command(state))
            response = Listener().send(interface, self.__get_command(state))
            if response == None:
                print ("response : None")
            else:
                if len(response) > 30:
                    print ("response : " + response[:30] + " ...")
                else:
                    print ("response : " + response)
            if response != None:
                state[self.__get_recv()] = response
        return state

    def run(self, state, interface):
        """
        Perform command(public method).

        :param: state State
        :param: interface A file path used as an interface between an agent and an external attack script.

        :return: Dict state
        """
        while not self.__is_done():
            state = self.__run_once(state, interface)

        return state
