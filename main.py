# -*- coding: utf-8 -*-
import heapq
import re
import time

from gensim.models import KeyedVectors, word2vec, Word2Vec
import multiprocessing
import jieba
import difflib
import data_process

# 数据源处理
data_process.process()

# 参数输入
result_amount = 3
input_word = input("请输入待匹配串:\n")
output_amount = int(input("请输入 top k:\n"))
r = "[A-Za-z0-9_.!+-=——,$%^，。？、~@#￥%……&*《》<>「」{}【】()/]"
input_word = re.sub(r, "", input_word)


# 计算运行时间
t1 = time.time()


# stopwords
def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf8').readlines()]
    return stopwords


stopwords = stopwordslist()

# input_word 分词
input_word_cut = []
cuts = jieba.cut(input_word, cut_all=False)
for cut in cuts:
    if cut not in stopwords and cut != '\n':
        input_word_cut.append(cut)

# 将input_word加入数据源
for i in input_word_cut:
    sentences = open(u'./data/result.txt')
    flag = 0
    for j in sentences:
        if i in j:
            flag = 1
    if flag == 0:
        open('data/result.txt', 'a', encoding='utf8').write(input_word_cut[i] + '\n')

# 数据源分词
sentences = open(u'./data/result.txt')
sentences_cut = []
for ele in sentences:
    cuts = jieba.cut(ele, cut_all=False)
    new_cuts = []
    for cut in cuts:
        if cut not in stopwords and cut != '\n':
            new_cuts.append(cut)
    sentences_cut.append(new_cuts)

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

# 模型训练
sentences = word2vec.Text8Corpus("data.txt")
# size是神经网络的隐藏层单元数，也就是后续每个词向量的维度，默认为100
model = Word2Vec(sentences, vector_size=256, min_count=1, window=5, sg=0, workers=multiprocessing.cpu_count())
model.save('word2vec.model')

# model.build_vocab(sentences, update=True)
# model.train(sentences, total_examples=model.corpus_total_words, epochs=10)

final_result = []

# 取得相似的数据
for i in range(0, len(input_word_cut)):
    similar = model.wv.most_similar(str(input_word_cut[i]), topn=result_amount)
    similar_words = []
    for j in range(0, result_amount):
        similar_words.append(similar[j][0])

    # 使用word2vec算法找寻相似的数据
    for j in range(0, result_amount):
        words = open(u'./data/result.txt')
        for word in words:
            if similar_words[j] in word:
                final_result.append(word)

    # 找寻与input_word分词之后相同的数据
    words = open(u'./data/result.txt')
    for new_word in words:
        if input_word_cut[i] in new_word:
            final_result.append(new_word)

# 数据去重
final_result = list(set(final_result))

# 计算相似度
similarity = []
for i in final_result:
    d = difflib.SequenceMatcher(None, input_word, str(i)).ratio() * 100
    similarity.append(d)

max_number = heapq.nlargest(output_amount, similarity)
max_index = []
similarity_result = []
for t in max_number:
    index = similarity.index(t)
    max_index.append(index)
    similarity_result.append(similarity[index])
    similarity[index] = 0

count = 0
for i in max_index:
    print("匹配结果：" + final_result[i], end="")
    print("相似度：%.2f" % similarity_result[count] + '%')
    count = count + 1

# 计算运行时间
t2 = time.time()
print("\n程序运行时间: %.4f" % (t2 - t1))
