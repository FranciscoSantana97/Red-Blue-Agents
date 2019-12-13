"""
Description
=====
Condition class is defined.
Condition is used to validate a state whether a state can satisfy a specific goal.
"""

import constant

class Condition():
    """
    Have a conditions to reflect a specific conditions(e.g. goal).
    """

    def __init__(self):
        self.conds = []
        pass

    def __str__(self):
        msg = "Condition ======\n"
        if len(self.conds) == 0:
            msg += "none\n"
        else:
            for e in self.conds:
                msg += " ".join(e) + "\n"
        msg += "===========\n"
        return msg

    def add(self, cond):
        """
        Add conditions

        :param cond: condition is a set which have 2 or 3 elements.
        The first is a key of a state, the second is a operator for checking condition.
        The third is an operand.
        """
        self.conds.append(cond)

    def is_satisfied(self, state):
        """
        Checks given state satisfy a condition that is defined in this instance.
        Every condition should be satisfied.

        :param state: A state to be checked.

        :return bool: True if a given state satisfy a condition otherwise False.
        """
        state_keys = list(state.keys())

        for e in self.conds:
            key = e[0]
            operator = e[1]

            if operator == constant.CONDITION_OPERATOR_EXIST:
                if not key in state_keys:
                    return False
            elif operator == constant.CONDITION_OPERATOR_NOT_EXIST:
                if key in state_keys:
                    return False
            else:
                if not key in state_keys:
                    return False

                value = e[2]
                state_value = state[key]
                if operator == constant.CONDITION_OPERATOR_EQUAL:
                    if not state_value == value:
                        return False
                elif operator == constant.CONDITION_OPERATOR_NOT_EQUAL:
                    if state_value == value:
                        return False
                elif operator == constant.CONDITION_OPERATOR_INCLUDE:
                    if value in state_value:
                        return True
                    return False
                else:
                    raise RuntimeError("Not implemented (" + operator + ")")

        return True

    def is_explorable(self, state):
        """
        Checks a given state satisfy a condition that is defined in this instance considering the concept of ASSUMED, which means that this method is used to generate plan, not to perform plan.

        :param state: A state to be checked.

        :return bool: True if a given state satisfy a condition otherwise False.
        """
        for e in self.conds:
            key = e[0]
            operator = e[1]
            try:
                value = e[2]
            except IndexError:
                value = None

            if operator == constant.CONDITION_OPERATOR_NOT_EXIST:
                if key in state:
                    return False
                continue

            if not key in state:
                return False

            if value == None:
                continue

            if state[key] == constant.STATE_VALUE_UNKNOWN:
                continue

            if value != state[key]:
                return False

        return True
