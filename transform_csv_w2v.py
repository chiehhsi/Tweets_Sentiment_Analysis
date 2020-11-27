import numpy as np
import os
from gensim.models import KeyedVectors
from scipy.spatial import distance

def read_file():
    file = 'https://github.com/felipebravom/AffectiveTweets/releases/download/1.0.0/w2v.twitter.edinburgh10M.400d.csv.gz'
    output_file = 'w2v.twitter.edinburgh10M.400d.txt'
    vocab_size = 258917
    embedding_dim = 400

    word2index = {}  # word to word-index
    embedding_matrix = np.zeros((vocab_size + 1, embedding_dim))
    idx = 1  # first row set to zero (for unknown words)

    with open(file, 'r', encoding='utf-8') as doc:
        line = doc.readline()
        while line != '':
            line = line.rstrip('\n').lower()
            data = line.split('\t')
            word = data[-1]
            coefs = np.asarray(data[:-1], dtype='float32')
            word2index[word] = idx
            embedding_matrix[idx] = np.asarray(coefs)
            idx += 1
            if idx % 1000 == 0:
                print(idx)
            line = doc.readline()

    print('Write word vectors to', output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, i in word2index.items():
            f.write(word)
            f.write(" ")
            f.write(" ".join(map(str, embedding_matrix[i])))
            f.write("\n")

def edin_word2vec_embeddings():
    original_file = 'w2v.twitter.edinburgh10M.400d.txt'
    word2vec_file = 'w2v.twitter.edinburgh10M.400d.txt.word2vec'
    if not os.path.exists(word2vec_file):
        from gensim.scripts.glove2word2vec import glove2word2vec
        glove2word2vec(original_file, word2vec_file)
    model = KeyedVectors.load_word2vec_format(word2vec_file, binary=False)
    # model.save_word2vec_format(word2vec_file + '.bin', binary=True)

if __name__ == '__main__':
    read_file()
    edin_word2vec_embeddings()
    print("pre-trained model generated")