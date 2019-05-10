##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## May 2019
##

from __future__ import print_function

class BaseSample :
    def __init__(self, sample_config = {}) :
        self._sample_config = sample_config
        self._name = ""
        self._input_files = []
        self._label = None
        self._weights = []
        self._tree_name = ""
        self._load_config(sample_config)

    @property
    def config(self) :
        return self._sample_config

    @property
    def name(self) :
        return self._name

    @property
    def input_files(self) :
        return self._input_files

    @property
    def label(self) :
        return self._label

    @property
    def weights(self) :
        return self._weights

    @property
    def dataset_name(self) :
        return self._tree_name

    @property
    def tree_name(self) :
        return self._tree_name

    def _load_config(self, config_dict = {}) :

        # validate the schema here
        self._name = config_dict["name"]
        self._input_files = config_dict["input_files"]
        self._label = int(config_dict["class_label"])
        self._weights = config_dict["weights"]
        self._tree_name = config_dict["tree_name"]

    def __str__(self) :
        out = "Sample -> name:              {}\n".format(self.name)
        out += "          input files:\n"
        n_f = len(self.input_files)
        for ifile, filename in enumerate(self.input_files) :
            out += "                             [%02d/%02d] %s\n" % (ifile+1, n_f, filename)
        out += "          train label:       {}\n".format(self.label)
        out += "          train weights:     {}\n".format(self.weights)
        return out
