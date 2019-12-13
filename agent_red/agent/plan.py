#!/usr/bin/python
"""
Description
=====
Two classes are defined.
Plan is for performing attacks sequences to satisfy the goal.
Planner is managing plans: generating plans, performing plans.
"""

from attackdb import AttackDB
from condition import Condition
import constant
import tempfile, os

def TEMP_print_state(state):
    msg = ""
    for e in state:
        if e == "binaries":
            msg += e + " : cron, wget, ...\n"
        else:
            msg += e + " : " + str(state[e]) + "\n"
    print (msg)
        
class Plan():
    """
    Managing attack sequence and related state.
    This class is unit of Planner.
    """

    def __init__(self, techs, state):
        """
        Constructor

        :param techs: A sequence of attacks.
        :param state: The state of the plan.
        """
        self.techs = techs
        self.static_state = state.copy()
        self.dynamic_state = None
        self.result = constant.PLAN_INIT
        self.idx = 0

    def __str__(self):
        msg = "Plan ==========\n"
        for i in range(0, len(self.techs)):
            msg += "[" + str(i) + "] " + \
                self.techs[i].name + "\n"
        #msg += "Static State : " + str(self.static_state) + "\n"
        #msg += "Dynamic State : " + str(self.dynamic_state) + "\n"
        msg += "Result : " + self.result + "\n"
        msg += "Last Technique : " + str(self.idx) + "\n"
        msg += "==============="
        return msg

    def __unique_tempfile(self):
        """
        Get Unique Temporary File Name (Not Secure)
        """
        file_path = ""
        dir_name = tempfile.gettempdir()
        while True:
            file_name = next(tempfile._get_candidate_names())
            file_path = os.path.join(dir_name, file_name)
            if not os.path.exists(file_path):
                break
        return file_path

    def is_satisfied(self, goal):
        """
        Checks whether the plan can satisfy the goal.

        :param goal: Condition of the goal.

        :return bool: True if the plan satisfy the goal, otherwise False.
        """
        return goal.is_explorable(self.static_state)

    def run(self, goal, state):
        """
        Run the plan until all attacks are performed or goal is satisfied.

        :param goal: Condition of the goal.
        :param state: Start state.

        :return bool: True if the plan satisfy the goal, otherwise False.
        """
        self.result = constant.PLAN_WORKING
        self.dynamic_state = state
        output = self.__unique_tempfile()

        print ("===== PLAN =====")
        print (self)

        while True:
            print ("====== STATE ======")
            TEMP_print_state(self.dynamic_state)

            if goal.is_satisfied(self.dynamic_state):
                print ("====== GOAL SATISFIED ======")
                self.result = constant.PLAN_SUCCEED
                break

            if len(self.techs) == self.idx:
                print ("===== ALL ATTACK WAS PERFORMED =====")
                self.result = constant.PLAN_FAIL
                break

            tech = self.techs[self.idx]
            print ("====== CHOOSEN TECHNIQUES ======")
            print (tech)
            if not tech.is_satisfied(self.dynamic_state):
                print ("CONDITION IS NOT SATISFIED")
                self.result = constant.PLAN_FAIL
                break

            self.dynamic_state = tech.run(output, self.dynamic_state)
            self.idx += 1

        print ("===== PLAN DONE =====")
        print (self)
        if self.result == constant.PLAN_SUCCEED:
            return True
        else:
            return False

class Planner():
    """
    Managing plans:Collect and run plans.
    """
    def __init__(self, state, goal):
        """
        Constructor

        :param state: A base state. Plans will be generated based on this state.
        :param goal: A base goal. Plans will be generated that achieve this goal.
        """
        self.plans = []
        self.state = state
        self.goal = goal

    def __str__(self):
        msg = "Planner =======\n"
        for i in range(0, len(self.plans)):
            msg += "Plan #" + str(i+1) + "\n"
            msg += str(self.plans[i])
        msg += "==============="
        return msg

    def __available_attacks(self, state, techs):
        """
        Collect available RTs whose precondition is satisfied by a given state.

        :param state: A current state.
        :param techs: All possible attacks.

        :return list: list for RTs.
        """
        nexts = []
        for e in techs:
            if e.is_explorable(state):
                nexts.append(e)
        return nexts

    def __explore_plans(self, state, techs, visits):
        """
        Collect available plans that can achieve the goal state.

        :param state: A current state.
        :param techs: All possible attacks.
        :param visits: Cumulated attacks.

        :return list: list for plans.
        """
        plans = []
        nexts = self.__available_attacks(state, techs)
        for e in nexts:
            local_state = state.copy()
            local_state = e.mark_explored(local_state)

            local_visits = visits[:]
            local_visits.append(e)

            local_techs = techs[:]
            local_techs.remove(e)

            plans += self.__explore_plans(local_state, local_techs, local_visits)

        plan = Plan(visits, state)
        if(plan.is_satisfied(self.goal)):
            plans.append(plan)

        return plans

    def make_plan(self):
        """
        Make plans that can achieve the goal state.
        """
        techs = AttackDB().get()
        local_state = self.state.copy()
        self.plans = self.__explore_plans(local_state, techs, [])

    def run(self):
        """
        Run plans that were prepared by \"make_plan\" method.
        Thus, make_plan should be called first.
        This method terminates when a certain scenario meet the goal state.

        :return bool: True if one of plans meets the goal state, otherwise False.
        """
        result = False
        for e in self.plans:
            if e.run(self.goal, self.state):
                result = True
                break

        for e in self.plans:
            if e.result == constant.PLAN_INIT:
                break
            else:
                print (e)

        return result
