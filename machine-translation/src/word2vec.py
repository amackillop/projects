import preprocessing
import utils

english = utils.unpickle_data('vocabs/OpenSubtitles2018.en-es.en.pickle')
spanish = utils.unpickle_data('vocabs/OpenSubtitles2018.en-es.es.pickle')

def get_word_maps(vocab, nwords):
    word2int = {word: i for i, (word, _) in enumerate(vocab.most_common(nwords))}
    int2word = {i: word for word, i in word2int_en.items()}
    return word2int, int2word

