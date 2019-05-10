#!/bin/env python

##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##

from __future__ import print_function
import argparse
import os, sys
import inspect

from .preprocessing import BasePreprocessor, DefaultPreprocessor

def get_hier(cls) :
    return inspect.getmro(cls.__class__)

def is_preprocessor(actor) :

    hier = get_hier(actor)
    for h in hier :
        if "basepreprocessor" in str(h).lower() :
            return True
    return False

def is_trainer(actor) :

    hier = get_hier(actor)
    for h in hier :
        if "basetrainer" in str(h).lower() :
            return True
    return False

def is_validator(actor) :

    hier = get_hier(actor)
    for h in hier :
        if "basevalidator" in str(h).lower() :
            return True
    return False

def classify_actors(input_actors = []) :

    preprocessors = []
    trainers = []
    validators = []

    for actor in input_actors :
        if is_preprocessor(actor) :
            preprocessors.append(actor)
        if is_trainer(actor) :
            trainers.append(actor)
        if is_validator(actor) :
            validators.append(validators)

    return preprocessors, trainers, validators

def learn(actors = [], models = []) :

    preprocessors, trainers, validators = classify_actors(actors)

    print("Loading {} preprocessors\n        {} trainers\n        {} validators".format(len(preprocessors), len(trainers), len(validators)))

if __name__ == "__main__" :
    pass
