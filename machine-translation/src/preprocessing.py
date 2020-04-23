import os
import math
import multiprocessing as mp
import collections
import itertools as it
import re
import pickle
from typing import Callable
from zipfile import ZipFile

import config
import utils

import nltk


def process_file(fname, nprocesses=mp.cpu_count()):
    """Process a file using multiprocessing."""
    with open(fname, 'r', encoding = 'iso-8859-1') as text:
        strands = utils.spagettify(text, nprocesses)
        result = utils.parallelize(build_vocab, strands)
        return result


def build_vocab(lines, result_queue):
    """Build a word count dictionary given an iterable of raw lines."""
    vocab = collections.Counter()
    chunks = utils.chunker(lines, 10000, '')
    for chunk in chunks:
        tokenizer = Tokenizer(chunk)
        vocab.update(tok for tok in tokenizer)
    result_queue.put(vocab)
    return vocab

def build_glove_vocab(vocab):
    with open('GloVe-1.2/vocab.txt', 'w', encoding='utf-8') as output:
        for key, value in sorted(vocab.items(), key=lambda x: x[1], reverse=True):
            output.write(f'{key} {value}\n')


def build_mapping(vocab, nwords):
    return {word: str(i) for i, (word, _) in enumerate(vocab.most_common(nwords))}


def clean_corpus(corpus):
    with open(corpus, 'r', encoding='iso-8859-1') as in_file:
        fname, _, ext = corpus.rpartition('.')
        with open(f'{fname}_clean.{ext}', 'w', encoding='iso-8859-1') as out_file:
            chunks = utils.chunker(in_file, 10000, '')
            for chunk in chunks:
                tokenizer = Tokenizer(chunk)
                for sent in tokenizer.yield_sentences():
                    out_file.write(sent + '\n')


def unzip_data(datasets, predicate: Callable[[str], bool]):
    zip_files = filter(predicate, os.listdir(datasets))
    for zip_file in zip_files:
        with ZipFile(f'{datasets}/{zip_file}', 'r') as zipped: 
            print(zipped.namelist())
            files = filter(predicate, zipped.namelist()) 
            for fname in files:
                print(fname)
                if not os.path.exists(f'{datasets}/{fname}'):
                    zipped.extract(fname, datasets) 


class Tokenizer(collections.abc.Generator):
    tokenizer = nltk.tokenize.wordpunct_tokenize

    def __init__(self, lines):
        str_chunk = self._remove_punc(' '.join(lines)).replace('\n', '.')
        self.token = None
        self.tokens = iter(self.tokenizer(str_chunk))

    def send(self, arg):
        self.token = self._clean(next(self.tokens))
        return self.token

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    @staticmethod
    def _clean(token):
        if token.strip().isdigit():
            return '#'
        elif token.strip() == '.':
            return '.'
        return token.lower()

    @staticmethod
    def _remove_punc(string):
        """Remove puncuation."""
        return re.sub(r'[^\w\s]', '', string)

    def _build_sentence(self):
        while True:
            try:
                next(self)
            except StopIteration:
                return
            yield self.token
            if self.token == '.':
                break

    def yield_sentences(self, mapping=None):
        """Generate sentences.

        If a mapping is provided, the sentences will be translated as per the map.

        """
        if mapping is None:
            def _map(x): return x
        else:
            def _map(x): return mapping.get(x, len(mapping))

        while True:
            sentence = ' '.join(str(_map(word)) for word in self._build_sentence())
            if sentence:
                yield sentence
            else:
                return


def main():
    """Build vocabularies if not present as a pickle file."""
    datasets = config.DATASETS
    vocabs = config.VOCABS
    unzip_data(datasets, lambda fname: fname.endswith('.en') or fname.endswith('.es'))
    source_files = filter(lambda fname: not fname.endswith('.zip'), os.listdir(datasets))
    for source in source_files:
        print(source)
        try:
            vocab = utils.unpickle_data(f'{vocabs}{source}.pickle')
        except FileNotFoundError:
            results = process_file(datasets + source)
            vocab = collections.Counter()
            for result in results:
                vocab.update(result)
            print(vocab)
            utils.pickle_data(vocab, f'{vocabs}{source}.pickle')
        build_glove_vocab(vocab)
        break

if __name__ == '__main__':
    print('starting')
    main()
    pass
