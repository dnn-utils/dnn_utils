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
import h5py
import numpy as np

from .preprocessing import BasePreprocessor, DefaultPreprocessor
from .sample import Sample
from .utils import dataset_utils as utils

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

def preprocess_sample(preprocessor, sample, input_group, training_size) :

    print("dnn_learn    Preprocessing sample {}".format(sample.name))

    features = preprocessor.input_features
    sample_ds = None
    fill_started = False
    for ifile, filename in enumerate(sample.input_files) :
        with h5py.File(filename, "r") as input_file :
            if sample.dataset_name not in input_file :
                raise Exception("Expected dataset (={}) not found in sample input file (={})".format(sample.dataset_name, filename))
            ds = input_file[sample.dataset_name]

            for ichunk, chunk in enumerate(utils.chunk_generator(ds)) :

                # don't continue looping if we're already maxed out
                if sample.label != 0 and fill_started and sample_ds.size >= training_size :
                    break

                # pass to the provided preprocessor
                chunk = preprocessor.preprocess(chunk)
    
                # extract only the requested features
                chunk = chunk[features]
                chunk = chunk[features]
    
                if not fill_started :
                    sample_ds = chunk[:]
                    fill_started = True
                else :
                    sample_ds = np.concatenate([sample_ds, chunk[:]])


    total_size = sample_ds.size
    if sample.label == 0 and training_size < 0 :
        training_size = int(float(total_size) / 2.0)
    elif sample.label != 0 and training_size < 0 :
        raise Exception("Training size is not set but we are processing an input file without label 0")
    ds_train = sample_ds[:training_size]
    ds_test = sample_ds[training_size:]

    # create the datasets in the output pre-processed file
    _ = input_group.create_dataset("train_features", shape = ds_train.shape,
                dtype = ds_train.dtype, data = ds_train, maxshape = (None,))
    _ = input_group.create_dataset("test_features", shape = ds_test.shape,
                dtype = ds_test.dtype, data = ds_test, maxshape = (None,))
    return training_size

def preprocess(preprocessor) :

    features = preprocessor.input_features
    n_features = len(features)
    print("dnn_learn    n_features: {}".format(n_features))

    # hardcode the output name for testing right now
    output_filename = "dnn_preprocessed.h5"
    with h5py.File(output_filename, "w") as outfile :
        sample_group = outfile.create_group("samples")
        training_size = -1
        for isample, sample in enumerate(preprocessor.samples) :
            class_group = sample_group.create_group(sample.name)
            class_group.attrs["class_label"] = sample.label
            training_size = preprocess_sample(preprocessor, sample, class_group, training_size)

    print("Storing preprocessed file: {}".format(os.path.abspath(output_filename)))
    return output_filename

def learn(actors = [], models = []) :

    preprocessors, trainers, validators = classify_actors(actors)

    print("Loading {} preprocessors\n        {} trainers\n        {} validators".format(len(preprocessors), len(trainers), len(validators)))

    if len(preprocessors) > 1 :
        raise Exception("Invalid number of preprocessors (={})".format(len(preprocessors)))

    if preprocessors :
        preprocessed_inputs = preprocess(preprocessors[0])

    


if __name__ == "__main__" :
    pass
