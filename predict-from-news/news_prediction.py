import os
import argparse
from typing import List, Iterable, Generator, Tuple

import pandas as pd
import allennlp.modules.elmo as elmo
import nltk
import torch

import config
import utils

# Reduce this if you run into memory issues.
CHUNK_SIZE = 250
def process_input_data():
    CSV_DATA = {}
    for fname in os.listdir(config.INPUT):
        CSV_DATA[fname] = pd.read_csv(config.INPUT + fname)


def load_elmo(options: str, weights: str) -> elmo.Elmo:
    """Loads an ELMo model."""
    return elmo.Elmo(options, weights, 2, dropout=0)


def tokenize(sentence: str) -> List[str]:
    """Take a sentence and return a list of tokens by word and puncuation.

    'Hello, World!' -> ['Hello', ',', 'World', '!']
    
    """
    tokenizer = nltk.tokenize.wordpunct_tokenize
    return tokenizer(sentence)


def process_sent_batches(sentences: Iterable[Tuple[str]]) -> Iterable[torch.Tensor]:
    """Tokenize sentences and convert to ids by batch."""
    for batch in sentences:
        tokenized = [tokenize(sent) for sent in batch]
        yield elmo.batch_to_ids(tokenized)


def get_sent_embeddings(id_batches: Iterable[torch.Tensor], model: elmo.Elmo):
    """Generalize for other models maybe?"""
    for batch in id_batch:
        yield model(batch)


def main():

    sentence_batches = utils.chunker(CSV_DATA['RedditNews.csv'].News, CHUNK_SIZE)
    character_ids = process_sent_batches(sentence_batches)

    options = config.MODELS + config.MODEL_FILE
    weights = config.MODELS + config.OPTIONS_FILE
    model = load_elmo(options, weights)

    embeddings = get_sent_embeddings(character_ids, model)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(input_file, 
    main()