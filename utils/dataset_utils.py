##
## author: Daniel Joseph Antrim <dantrim1023@gmail.com>
##                              <daniel.joseph.antrim@cern.ch>
## date: May 2019
##


def chunk_generator(input_h5_dataset, chunksize = 100000) :
    for x in range(0, input_h5_dataset.size, chunksize) :
        yield input_h5_dataset[x:x+chunksize]
