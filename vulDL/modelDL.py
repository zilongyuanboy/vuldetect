# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   modelDL.py
@Author     :   zilongyuan
@datetime   :    2023/2/18
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""
import gc

import torch
import numpy as np
import pandas as pd
from vulDL.mapping import *

import os

def process_data(data, method="test"):
    '''
    处理并清洗切片数据
    :param data: 文件的切片字符串
    :type data: str
    :return: 清洗后的切片数组[corpus, labels, focus, funcs, filenames]
    :rtype: list
    '''
    # slicelists
    slicelists = data.split('-'*30)
    if slicelists[0] == '':
        del slicelists[0]
    if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n' or slicelists[-1] == "\'":
        del slicelists[-1]

    # process slices
    lastprogram_id = 0
    program_id = 0
    index = -1
    slicefile_corpus = []
    slicefile_labels = []
    slicefile_focus = []
    slicefile_filenames = []
    slicefile_funcs = []
    focuspointer = None

    for slicelist in slicelists:
        slice_corpus = []
        focus_index = 0
        flag_focus = 0
        index = index + 1
        # process single slice to multi sentences
        sentences = slicelist.replace('\r\n', '\n').split('\\n')  # 这里换行符好像要转义
        if sentences[0] == '\r' or sentences[0] == '' or sentences[0] == '\r\n' or sentences[0] == "b'":
            del sentences[0]
        if sentences == []:
            continue
        if sentences[-1] == '' or sentences[-1] == '\r' or sentences[-1] == '\r\n':
            del sentences[-1]
        focuspointer = sentences[0].split(" ")[-2:]
        sliceid = index
        file_name = sentences[0]

        program_id = sentences[0].split(" ")[1].split("/")[-1]
        if lastprogram_id == 0:
            lastprogram_id = program_id
        # if not(lastprogram_id == program_id):  # 项目不相等就不执行
        if method == 'test':
            sentences_label = sentences[-1]
            sentences = sentences[1:-1]
        else:
            sentences_label = 'UNK'
            sentences = sentences[1:]
        for sentence in sentences:
            if focuspointer[0] in sentence.split(' ') and flag_focus == 0:
                flag_focus = 1
            start = str.find(sentence, r'printf("')
            if start != -1:
                # cut printf("..."); func
                start = str.find(sentence, r'");')
                sentence = sentence[:start+2]
            fm = str.find(sentence, '/*')
            if fm != -1:
                # strip annotation /**/
                sentence = sentence[:fm]
            else:
                fm = str.find(sentence, '//')
                if fm != -1:
                    # strip annotaion //
                    sentence = sentence[:fm]
            sentence = sentence.strip()
            # 切分token
            list_tokens = create_tokens(sentence)
            if flag_focus == 1:
                # find focus
                focus_index = focus_index + list_tokens.index(focuspointer[0])
                flag_focus = 2
                slicefile_focus.append(focus_index)
            # elif flag_focus == 2:
            #     focus_index = len(list_tokens) // 2
            #     flag_focus = 2
            #     slicefile_focus.append(focus_index)
            slice_corpus = slice_corpus + list_tokens
        if flag_focus != 2:
            focus_index = focus_index + len(slice_corpus)//2
            slicefile_focus.append(focus_index)
        slicefile_labels.append(sentences_label)
        slicefile_filenames.append(file_name)

        # 自变量、函数映射 <===== 这里有点问题
        slice_corpus, slice_func = mapping(slice_corpus)
        slice_func = list(set(slice_func))
        if slice_func == []:
            slice_func = ['main']
        sample_corpus = []
        for sentence in slice_corpus:
            # 切分token
            list_tokens = create_tokens(sentence)
            sample_corpus = sample_corpus + list_tokens
        slicefile_corpus.append(sample_corpus)
        slicefile_funcs.append(slice_func)
    dataset = [slicefile_corpus,
               slicefile_labels,
               slicefile_focus,
               slicefile_funcs,
               slicefile_filenames]
    # dataset_path = './temp/corpus/' + ''
    return dataset

def load_prodata(rawfile, save=False):
    '''
    加载并预处理上传的切片数据
    :param rawfile: 未处理的上传数据
    :type rawfile: file
    :param save: 是否存储文件数据
    :type save: bool
    :return: 处理后的数据[corpus, lables, focus, funcs, filenames], 如果上传数据不包含labels，则其值未"UNK"
    :rtype: list
    '''
    # save temp file
    if save:
        temp_file_path = os.path.join('./temp/files/', rawfile.name())
        if not os.path.exists(os.path.dirname(temp_file_path)):
            os.makedirs(os.path.dirname(temp_file_path))
        with open(temp_file_path, 'wb+') as tmpfile:
            for chunk in rawfile.chunks():
                tmpfile.write(chunk)
    rawdata = []
    for chunk in rawfile.chunks():
        rawdata.append(str(chunk))
    data = ''.join(rawdata)
    dataset = process_data(data)
    if save:
        temp_corpus_path = os.path.join('./temp/corpus/', rawfile.name())
        if not os.path.exists(os.path.dirname(temp_corpus_path)):
            os.makedirs(os.path.dirname(temp_corpus_path))
        f = open(temp_corpus_path, 'wb')
        pickle.dump(dataset, f)
        f.close()
    return dataset


from gensim.models.word2vec import Word2Vec
'''
Dir of corpus class
-------------------------
This class is used to make a generator to produce sentence for word2vec training

# Arguments
    dirname: The src of corpus files
'''
class DirofCorpus(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for d in self.dirname:
            for fn in os.listdir(d):
                if not os.path.isdir(os.path.join(d, fn)):
                    continue
                for filename in os.listdir(os.path.join(d, fn)):
                    samples = pickle.load(open(os.path.join(d, fn, filename), 'rb'))[0]
                    for sample in samples:
                        yield sample  # 切片的一行 sentence
                    del samples
                    gc.collect()

def generate_w2vModel(decTokenFlawPath, w2vModelpath):
    '''
    generate w2vmodel function, This function is usec to learning vectors from corpus, and save the model
    :param decTokenFlawPath: dir of corpus
    :type decTokenFlawPath: str
    :param w2vModelpath: save dir of w2vmodel
    :type w2vModelpath:  str
    :return:  None
    :rtype:  None
    '''
    model = Word2Vec(sentences=DirofCorpus(decTokenFlawPath),
                     size=30, alpha=0.01, window=5, min_count=0,
                     max_vocab_size=None, sample=0.001, seed=1,
                     workers=1, min_alpha=0.0001, sg=1, hs=0,
                     negative=10, iter=5)
    model.save(w2vModelpath)


# from get_dl_input_vector import *
def load_w2vmodel(w2vModelPath, slicelists):
    '''
    将一个切片语料处理成向量
    :param w2vModelPath: 词向量模型路径
    :type w2vModelPath: str
    :param samples:  切片语料集
    :type samples: list
    :return: 切片向量
    :rtype: list [[[corpus], labels, filename, func, focus]], ..., [[],...]]
    '''
    model = Word2Vec.load(w2vModelPath)
    for i in range(len(slicelists)):
        slicelists[i][0] = [[model[word] if word in model.wv.index2word else model[-1] for word in sample] for sample in slicelists[i]]
    return slicelists

def get_vector(w2vModelPath, slicelists):
    if not os.path.isfile(w2vModelPath):
        corpusfile = './vulDL/temp/corpus/'
        generate_w2vModel(corpusfile, w2vModelPath)
    else:
        return load_w2vmodel(w2vModelPath, slicelists)


def fix_vector(slicelists, maxlen=None, vector_dim=30):
    '''
    固定切片长度以输入深度学习预测模型中
    :param slicelists: 含有语料转化向量后的切片list
    :type slicelists: list
    :return: 含有语料转化向量后的固定切片长度的list [[X], [labels], [funcs], [filenames]]
    :rtype: list
    '''
    X, ids, focus, funcs, filenames = slicelists
    cut_count = 0
    fill_0_count = 0
    no_change_count = 0
    fill_0 = [0] * vector_dim
    totallen = 0
    if maxlen:
        new_X = []
        for x, i, focu, func, file_name in zip(X, ids, focus, funcs, filenames):
            if len(x) < maxlen:  # 切片不够固定长度，直接填0扩充
                x = x + [fill_0] * (maxlen - len(x))
                new_X.append(x)
                fill_0_count += 1
            elif len(x) == maxlen:
                new_X.append(x)
                no_change_count += 1
            else:
                # 切片超过固定长度的，以focu为中心砍掉前后多余部分
                startpoint = int(focu - round(maxlen / 2.0))
                endpoint = int(startpoint + maxlen)
                if startpoint < 0:
                    # focu 在x中靠前
                    startpoint = 0
                    endpoint = maxlen
                if endpoint >= len(x):
                    # focu 在x中靠后
                    startpoint = -maxlen
                    endpoint = None
                new_X.append(x[startpoint:endpoint])
                cut_count += 1
            totallen = totallen + len(x)
        X = new_X
    return X, ids, funcs, filenames,


# def build_model(maxlen, vector_dim, layers, dropout):
#     model = torch.nn.Sequential()
#     model.add_module(torch.nn.Module)

def generate_bgrumodel(bgruModelPath):  # <=======?
    pass

from .Bgru import DiyBgru
def load_model(bgruModelPath):
    if not os.path.isfile(bgruModelPath):
        generate_bgrumodel(bgruModelPath)
    else:
        model = DiyBgru(input_dim=30, hidden_size=20, out_size=2)
        model.load_state_dict(torch.load(bgruModelPath))
        return model

def vulPredict(rawfile):
    """
    输入预测文件，并以字符串的形式返回结果
    :param rawfile: file
    :type rawfile:
    :return: result
    :rtype: str ?
    """
    slicelists = load_prodata(rawfile)  # 这里的mapping可以去掉？
    # w2vmodel = load_w2vmodel()
    w2vmodelpath = './vulDL/temp/model/wordmodel'
    slicelists[0] = get_vector(w2vmodelpath, slicelists)  #
    X, y, funcs, filenames = fix_vector(slicelists, maxlen=50, vector_dim=30)
    bgrumodelpath = './vulDL/temp/model/bgrumodel'
    model = load_model(bgrumodelpath)
    res = model.predicit()
    return "vulDL"