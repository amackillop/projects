"""
Global script parameters live here.

This keeps the scripts in sync.

"""

INPUT = 'input/'
MODELS = 'models/'

MODEL_URLS = {
    'elmo_original_5.5.hdf5': 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_weights.hdf5',
    'elmo_original_5.5_config.json': 'https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_options.json'
    }   

MODEL_FILE = [fname for fname in MODEL_URLS.keys() if '.hdf5' in fname][0]
OPTIONS_FILE = [fname for fname in MODEL_URLS.keys() if '.json' in fname][0]