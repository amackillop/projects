# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 16:18:48 2018

@author: Austin

"""
import nltk
import itertools
from multiprocessing import Pool
import os
import pickle
import collections
import re
import functools
import collections

def chunker(iterable, chunk_size, fillvalue=None):
    """Yield `chunk_size` tuples of values from any iterable."""
    args = [iter(iterable)] * chunk_size
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def file_chunker(fname, chunk_size, encoding='utf-8', nchunks=None):
    """Yield `chunk_size` tuples of lines from a file."""
    with open(fname, 'r', encoding=encoding) as raw_data:
        line_chunker = chunker(raw_data, chunk_size, fillvalue='')
        n = itertools.count()
        for lines in line_chunker:
            if nchunks and next(n) >= nchunks:
                raise StopIteration
            yield lines

def remove_punc(string):
    """Remov puncuation but keep periods."""
    return re.sub('[^\w\s.]','', string)

def build_vocab(line_chunks):
    vocab = collections.Counter()
    for chunk in line_chunks:
        chunk_str = remove_punc(' '.join(chunk))
        tokenizer = Tokenizer(chunk_str)
        vocab.update(tok for tok in tokenizer)
    return vocab

def build_word_maps(vocab, vocab_size=None):
    word_to_int = {word: i for i, (word, _) in enumerate(vocab.most_common(vocab_size))}
    word_to_int['<UNK>'] = len(word_to_int)
    int_to_word = {i: word for word, i in word_to_int.items()}
    return word_to_int, int_to_word

def translate_text_to_int(text, out_file, mapping, encoding='utf-8'):
    with open(out_file, 'w', encoding=encoding) as output:
        for chunk in text:
            string_chunk = remove_punc(' '.join(chunk))
            tokenizer = Tokenizer(string_chunk)
            sentences = (sentence for sentence in tokenizer.yield_sentences(mapping))
            output.writelines(sentences)
        
def process_file(fname, vocab_size):
    text = file_chunker(fname, 100000)
    vocab = build_vocab(text)
    word_to_int, int_to_word = build_word_maps(vocab, vocab_size)
    text = file_chunker(fname, 100000)
    translate_text_to_int(text, 'test2.txt', word_to_int)
#    pickle_data(vocab, 'vocabs/' + fname.rpartition('/')[-1])
    return word_to_int, int_to_word

def pickle_data(data, fname):
    with open(fname + '.pickle', 'wb') as pfile:
        pickle.dump(data, pfile, protocol=pickle.HIGHEST_PROTOCOL)
        
def unpickle_data(fname):
    with open(fname, 'rb') as pfile:
        data = pickle.load(pfile)
    return data
        
        
def main():
    folder = 'EU-parl/'
    files = [folder + fname for fname in os.listdir(folder)]
    with Pool(2) as p:
        p.map(process_file, files)
            
class Tokenizer(collections.Generator):
    tokenizer = nltk.tokenize.wordpunct_tokenize
    
    def __init__(self, string_chunk):
        self.token = None
        self.tokens = iter(self.tokenizer(string_chunk))
    
    def send(self, arg):
        self.token = self._clean(next(self.tokens))
        return self.token
    
    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration
        
    def _clean(self, token):
        if token.strip().isdigit():
            return '<NUM>'
        elif token.strip() == '.':
            return '<EOS>'
        return token.lower()
        
    def _build_sentence(self):
        while next(self) != '<EOS>':
            yield self.token
        yield self.token
    
    def yield_sentences(self, mapping=None):
        def mapper(mapping):
            if mapping is None:
                return (lambda x: x)
            else:
                return (lambda x: mapping.get(x, len(mapping)-1))
            
        _map = mapper(mapping)
        while True:
            sentence = ' '.join(str(_map(word)) for word in self._build_sentence())
            if sentence:
                yield sentence + '\n'
            else:
                raise StopIteration
        
if __name__ == '__main__':
#    main()
    pass