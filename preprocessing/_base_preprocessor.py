##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##

from __future__ import print_function
from abc import ABC, abstractmethod
import os, sys
import json

from dnn_utils.sample import Sample

class BasePreprocessor(ABC) :
    def __init__(self, config_file = "") :
        super().__init__()

        self._name = ""
        self._samples = []
        self._input_features = []
        self._regress_features = []

        self._config_file = config_file
        self._load_config(config_file)

    @property
    def config(self) :
        return self._config_file

    @property
    def samples(self) :
        return self._samples

    @property
    def input_features(self) :
        return self._input_features

    def _load_config(self, config_file = "") :

        if not os.path.isfile(config_file) :
            raise Exception("Input configuration file (={}) not found".format(config_file))

        # we should place the JSON scheme check here

        with open(config_file, "rb") as json_input :
            data = json.load(json_input)

        config_name = data["name"]
        input_classes = data["input_classes"]
        input_feature_names = data["input_features"]
        regress_features = []
        if "regress_features" in data :
            regress_features = data["regress_features"]
        event_index_feature_name = ""
        if "event_index_string" in data :
            event_index_feature_name = data["event_index_string"]

        for input_class in input_classes :
            s = Sample(input_class)
            self._samples.append(s)

        for feature in input_feature_names :
            self._input_features.append(feature)
            
        print("Loaded configuration from file: {}".format(config_file))
        print(" name: {}\n input classes: {}\n n train features: {}".format(config_name, [x["name"] for x in input_classes], len(input_feature_names)))

    @abstractmethod
    def preprocess(self, arr) :
        pass

   # @classmethod
   # def __subclasshook__(cls, C) :
   #     print("mro: {}".format(C.__mro__))
