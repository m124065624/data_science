# -*- coding: utf-8 -*-
import heapq
import time

from gensim.models import KeyedVectors, word2vec, Word2Vec
import multiprocessing
import jieba
import difflib

result_amount = 3
output_amount = 10
input_word = '采矿权人姓名'
sentences = open(u'./data/result.txt')
flag = 0
for i in sentences:
    if input_word in i:
        flag = 1
if flag == 0:
    open('data/result.txt', 'a', encoding='utf8').write(input_word + '\n')

# 计算运行时间
t1 = time.time()


def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf8').readlines()]
    return stopwords


sentences = open(u'./data/result.txt')
stopwords = stopwordslist()
sentences_cut = []
for ele in sentences:
    cuts = jieba.cut(ele, cut_all=False)
    new_cuts = []
    for cut in cuts:
        if cut not in stopwords and cut != '\n':
            new_cuts.append(cut)
    sentences_cut.append(new_cuts)
print(sentences_cut)

# 分词后的文本保存在data.txt中
with open('data.txt', 'w') as f:
    for ele in sentences_cut:
        s = str(ele)
        result = ''
        for i in s:
            if i != '[' and i != ']' and i != '\'':
                if i == ',':
                    i = '\n'
                elif i == ' ':
                    i = ""
                result += i
        f.write(result + '\n')

sentences = word2vec.Text8Corpus("data.txt")
print(sentences)
# size是神经网络的隐藏层单元数，也就是后续每个词向量的维度，默认为100
model = Word2Vec(sentences, vector_size=256, min_count=1, window=5, sg=0, workers=multiprocessing.cpu_count())
model.save('word2vec.model')
print(model)

# model.build_vocab(sentences, update=True)
# model.train(sentences, total_examples=model.corpus_total_words, epochs=10)

# get top 3 similar words
similar = model.wv.most_similar([input_word], topn=result_amount)
print(similar)
similar_words = []
for i in range(0, result_amount):
    # print(i)
    similar_words.append(similar[i][0])
    # print(similar_words.append(similar[i][0]))
# print(similar_words)

t2 = time.time()
final_result = []
# get the sentences in result.txt
for i in range(0, result_amount):
    words = open(u'./data/result.txt')
    for word in words:
        if similar_words[i] in word:
            final_result.append(word)

similarity = []
for i in final_result:
    d = difflib.SequenceMatcher(None, input_word, str(i)).ratio() * 100
    similarity.append(d)

max_number = heapq.nlargest(output_amount, similarity)
max_index = []
for t in max_number:
    index = similarity.index(t)
    max_index.append(index)
    similarity[index] = 0

for i in max_index:
    print(final_result[i])

print("Loading time: %.4f" % (t2 - t1))
