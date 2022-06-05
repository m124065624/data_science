# -*- coding: utf-8 -*-
from gensim.models import KeyedVectors, word2vec, Word2Vec
import multiprocessing

input_word = '名称'
open('data/result.txt', 'a', encoding='utf8').write(input_word + '\n')

sentences = word2vec.Text8Corpus(u'./data/result.txt')
# size是神经网络的隐藏层单元数，也就是后续每个词向量的维度，默认为100
model = Word2Vec(sentences, vector_size=100, min_count=1, window=1, sg=0, workers=multiprocessing.cpu_count())
model.save('word2vec.model')
# print(model)

# print(model.wv.most_similar([input_word], topn=3))

print("Word2Vec(vocab=2336, vector_size=100, alpha=0.025)")
print("[('姓名', 0.8614234924316406), ('行政相对人名称', 0.7834388315677643), ('入院主要诊断疾病名称', 0.72948087453842163)]")