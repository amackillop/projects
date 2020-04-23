import os

# Necessary directories
DATASETS = 'data/'
VOCABS = 'vocabs/'
GLOVE = 'GloVe-1.2'

if not os.path.exists(DATASETS):
    os.mkdir(DATASETS)

if not os.path.exists(VOCABS):
    os.mkdir(VOCABS)

if not os.path.exists(GLOVE):
    os.mkdir(GLOVE)
