##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##

from __future__ import print_function

from abc import ABC, abstractmethod

class BaseModel(ABC) :
    def __init__(self) :
        super().__init__()
        self._model = None

    @property
    def model(self) :
        return self._model
    @model.setter
    def model(self, model = None) :
        self._model = model

    @abstractmethod
    def print_name(self) :
        pass
