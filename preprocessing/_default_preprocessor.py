##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##

from __future__ import print_function

from ._base_preprocessor import BasePreprocessor

class DefaultPreprocessor(BasePreprocessor) :

    def __init__(self, config_file = "") :
        super().__init__(config_file)

    def preprocess(self, arr) :
        # default is a pass through
        input_size = arr.size
        output_size = arr.size
        print("DefaultPreprocessor::preprocess  Input size = {}, Output size = {}".format(input_size, output_size))
        return arr
