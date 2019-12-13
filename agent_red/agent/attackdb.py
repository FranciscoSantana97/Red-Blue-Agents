"""
Description
=====

A temporal module for storing attack data
"""

import os, constant
from rt import RT
from condition import Condition
from singleton import Singleton

DB_RECORDS = [
        {
            "Name" : "nmap for searching open ports",
            "Preconditions" : [
                ("protocol", "EQ", "ip"),
                ("address", "EXIST"),
                ("ports", constant.CONDITION_OPERATOR_NOT_EXIST),
            ],
            "Postconditions" : [
                ("os", "UNKNOWN"),
                ("ports", "UNKNOWN")
            ],
            "Command" : "attacks" + os.sep + "nfsop" + os.sep + "cmd.json",
        },
        {
            "Name" : "CVE-2015-5958 for RCE(unix)",
            "Preconditions" : [
                ("os", "EQ", "linux"),
                ("address", "EXIST"),
                ("protocol", "EXIST"),
                ("ports", "EXIST"),
                ("shell", constant.CONDITION_OPERATOR_NOT_EXIST)
            ],
            "Postconditions" : [
                ("shell", "TEMPORAL")
            ],
            "Command" : "attacks" + os.sep + "cve20155958" + os.sep + "cmd.json",
        },
        {
            "Name" : "CVE-2016-3714 for RCE(unix)",
            "Preconditions" : [
                ("os", "EQ", "linux"),
                ("address", "EXIST"),
                ("protocol", "EXIST"),
                ("ports", "EXIST"),
                ("shell", constant.CONDITION_OPERATOR_NOT_EXIST)
            ],
            "Postconditions" : [
                ("shell", "TEMPORAL")
            ],
            "Command" : "attacks" + os.sep + "cfru" + os.sep + "cmd.json",
        },
        {
            "Name" : "System Investigation(unix)",
            "Preconditions" : [
                ("os", "EQ", "linux"),
                ("shell", "EXIST"),
                ("binaries", constant.CONDITION_OPERATOR_NOT_EXIST),
                ("privilege", constant.CONDITION_OPERATOR_NOT_EXIST)
            ],
            "Postconditions" : [
                ("binaries", "UNKNOWN"),
                ("privilege", "UNKNOWN"),
                ("cwd", "UNKNOWN"),
            ],
            "Command" : "attacks" + os.sep + "siu" + os.sep + "cmd.json",
        },
        {
            "Name" : "Download(wget)",
            "Preconditions" : [
                ("shell", "EQ", "TEMPORAL"),
                ("binaries", "INCLUDE", "wget")
            ],
            "Postconditions" : [
                ( "shell", "DOWNLOADED" ),
            ],
            "Command" : "attacks" + os.sep + "dw" + os.sep + "cmd.json",
        },
        {
            "Name" : "Install(cron)",
            "Preconditions" : [
                ("shell", "EQ", "DOWNLOADED"),
                ("binaries", "INCLUDE", "cron"),
                ("privilege", "EQ", "0"),
                ("cwd", "EXIST")
            ],
            "Postconditions" : [
                ( "shell", "PERMANENT" ),
            ],
            "Command" : "attacks" + os.sep + "ic" + os.sep + "cmd.json",
        },
        {
            "Name" : "Misconfiguration_Investigation(sudo)",
            "Preconditions" : [
                ("shell", "EXIST"),
                ("binaries", "INCLUDE", "sudo"),
                ("privilege", "NEQ", "0"),
            ],
            "Postconditions" : [
                ( "misudo", "UNKNOWN" ),
            ],
            "Command" : "attacks" + os.sep + "misudo" + os.sep + "cmd.json"
        },
        {
            "Name" : "Exploit_Misconfiguration(sudo find)",
            "Preconditions" : [
                ("shell", "EXIST"),
                ("binaries", "INCLUDE", "sudo"),
                ("misudo", "INCLUDE", "sudofind"),
                ("privilege", "NEQ", "0"),
            ],
            "Postconditions" : [
                ( "privilege", "0")
            ],
            "Command" : "attacks" + os.sep + "emsudofind" + os.sep + "cmd.json"
        }
    ]
"""
A constant array for storing attack data.
Later, it is recommended to store these externally.

Each data has 4 values.
The followings are detailed description for each value.

[1] Name: A name of attack, that is only used for logging for helping user to identify an attack.

[2] Preconditions: Array for specifying pre-conditions that should be satisfied to trigger an attack.
The format of each element of condition: (\"key\", \"operator\", \"value\").

    - key: This element is used as a key of state.
    - operator: Operators for a condition. Belows are available conditions.
        - EXIST: True when \"key\" is specified in a state.
        - NOT EXIST: True when \"key\" is not specified in a state.
        - EQ: True when a value of \"key\" in a state is the same as \"value\".
        - NEQ: True when a value of \"key\" in a state is not the same as \"value\".
        - INCLUDE: True when a value of \"key\" in a state includes \"value\".
    - value: A value to check conditions. Some operators may not require this value (e.g. EXIST).

[3] Postconditions: Array for specifying post-conditions that are expected to be satisfied after an attack.
The format of each element of condition: (\"key\", \"value\").

    - key: This element is used as a key of state.
    - value: A value to be assigned to a state.
        - UNKNOWN: Some values are unknown to an agent before actual attack is performed. (e.g. os).
In this case, UNKNOWN is assigned that is used to connect each attack to one available scenario.

[4] Command: A path to a file that stores commands to perform an attack.
This file has its own format, that is explained in other documents.
"""

#This class should be implemented as a real DB on the non-volatile system.
class AttackDB(Singleton):
    """
    A manager of attack records (Singleton Class).
    Every attack record can be accessed through this class.
    """

    #__instance = None
    __records = []
    """ Class variables for storing attack records.
    """

    def __str__(self):
        msg = "AttackDB ===========\n"
        if len(self.__records) == 0:
            msg += "None\n";
        else:
            for i in range(0, len(self.__records)):
                msg += "[" + str(i+1) + "] " + str(self.__records[i])
        msg += "===================\n"
        return msg

    def update(self):
        """
        Storing each attack records into __records in an instance of this class.
        An attack record is stored in there as an instance of RT class.
        """
        global DB_RECORDS
        for e in DB_RECORDS:
            keys = list(e.keys())

            if not "Name" in keys or not "Preconditions" in keys \
                or not "Postconditions" in keys or not "Command" in keys:
                print ("INVALID RECORD :\n" + str(e) + "\n")
                continue

            name = e["Name"]
            cond = Condition()
            for pre in e["Preconditions"]:
                cond.add(pre)
            post = e["Postconditions"]
            cmd = e["Command"]
            self.__records.append(RT(name, cond, post, cmd))

    def get(self):
        """
        Providing every attack records

        :return list: RT instances.
        """
        return self.__records

    def get_availables(self, state):
        """
        Providing available attack records that can be triggered based on a provided state.

        :param state: Dictionary that used as a state.

        :return list: RT instances.
        """
        ret = []
        for e in self.__records:
            if e.is_satisfied(state):
                ret.append(e)
        return ret
