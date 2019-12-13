"""
Description
======
This module is a super class for classes who is defined as a singleton class.
"""

class Singleton(object):
    """
    Singleton class that is only used as a super class for a classes that need to be defined as a singleton class.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
