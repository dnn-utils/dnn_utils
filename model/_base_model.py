##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##

from __future__ import print_function

from abc import ABC, abstractmethod
print("ABC: {}".format(ABC))

class BaseModel :
    def __init__(self) :
        print("BaseModel initialization")
