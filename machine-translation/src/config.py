import os

DATASETS = 'datasets/'
VOCABS = 'vocabs/'

if not os.path.exists(DATASETS):
    os.mkdir(DATASETS)

if not os.path.exists(VOCABS):
    os.mkdir(VOCABS)