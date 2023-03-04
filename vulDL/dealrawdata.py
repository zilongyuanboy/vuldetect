## coding: utf-8
'''
This python file is used to train data in CNN model
'''

from __future__ import absolute_import
from __future__ import print_function
import pickle
# import cPickle
import numpy as np
import random
import time
import math
import os
from collections import Counter

# ==> 下面好像没有用到，但是保留的话又会报错，没有该模块，故注释掉
# from imblearn.ensemble import BalanceCascade
# from imblearn.over_sampling import ADASYN
# from imblearn.over_sampling import SMOTE
# <==

np.random.seed(1337)  # for reproducibility

'''
dealrawdata function
-----------------------------
This function is used to cut the dataset, do shuffle and save into pkl file.

# Arguments
    raw_traindataSet_path: String type, the raw data path of train set
    raw_testdataSet_path: String type, the raw data path of test set
    traindataSet_path: String type, the data path to save train set
    testdataSet_path: String type, the data path to save test set
    batch_size: Int type, the mini-batch size
    maxlen: Int type, the max length of data
    vector_dim: Int type, the number of data vector's dim

'''
def dealrawdata(raw_traindataSet_path, raw_testdataSet_path, traindataSet_path, testdataSet_path, batch_size, maxlen, vector_dim):
    print("Loading data...")
    
    for filename in os.listdir(raw_traindataSet_path):
        if not (filename.endswith(".pkl")):
            continue
        print(filename)
        X_train, train_labels, funcs, filenames, testcases = load_data_binary(raw_traindataSet_path + filename, batch_size, maxlen=maxlen, vector_dim=vector_dim)

        f_train = open(traindataSet_path + filename, 'wb')
        pickle.dump([X_train, train_labels, funcs, filenames, testcases], f_train)
        f_train.close()

    for filename in os.listdir(raw_testdataSet_path):
        if not ("api" in filename):
            continue
        print(filename)
        if not (filename.endswith(".pkl")):
            continue
        X_test, test_labels, funcs, filenames, testcases = load_data_binary(raw_testdataSet_path + filename, batch_size, maxlen=maxlen, vector_dim=vector_dim)

        f_test = open(testdataSet_path + filename, 'wb')
        pickle.dump([X_test, test_labels, funcs, filenames, testcases], f_test)
        f_test.close()

def load_data_binary(dataSetpath, batch_size, maxlen=None, vector_dim=40, seed=113):   
    #load data
    f1 = open(dataSetpath, 'rb')
    X, ids, focus, funcs, filenames, test_cases = pickle.load(f1)
    f1.close()
	
    cut_count = 0
    fill_0_count = 0
    no_change_count = 0
    fill_0 = [0]*vector_dim
    totallen = 0
    if maxlen:
        new_X = []
        for x, i, focu, func, file_name, test_case in zip(X, ids, focus, funcs, filenames, test_cases):
            if len(x) <  maxlen:  # ==> 当切片向量不够maxlen=500时，直接填0填充，但是有个问题是之前的词向量维度是30，后面填充的0向量维度是40，也就是500个词，前面的词dim=30， 后面填充的o(词)dim=40
                x = x + [fill_0] * (maxlen - len(x))
                new_X.append(x)
                fill_0_count += 1

            elif len(x) == maxlen:  # ==> 切片向量刚好是maxlen=500时，则不做处理，原封保存
                new_X.append(x)
                no_change_count += 1
                    
            else:  # ==> 切片向量超过maxlen=500时，则删掉超过的部分
                startpoint = int(focu - round(maxlen / 2.0))  # ==> 记录focu前面的词向量长度
                endpoint =  int(startpoint + maxlen)  # ==> 记录focu后面的词向量长度，相当于endpoint = int(focu + maxlen/2)
                if startpoint < 0:  # ==> 如果切片向量超过maxlen=500，同时漏洞点(爆发行)focu前面的部分不足maxlen=500的一半，则说明focu后面的部分超过maxlen=500的一半，删除focu后面的多余部分
                    startpoint = 0  # ==> 取x[0:maxlen]
                    endpoint = maxlen
                if endpoint >= len(x):  # ==> 如果切片向量超过maxlen=500，同时漏洞点(爆发行)focu后面的部分不足maxlen=500的一半，则说明focu前面的部分超过maxlen=500的一半，删除focu前面的多余部分；理解：endpoint=focu + maxlen/2，len(x) = focu + focu后面的部分，故endpoint >= len(x) 相当于maxlen/2 >= focu 后面的部分
                    startpoint = -maxlen  # ==> 相当于从后往前数，取x[-maxlen:]
                    endpoint = None
                new_X.append(x[startpoint:endpoint])
                cut_count += 1
            totallen = totallen + len(x)
    X = new_X
    print(totallen)

    return X, ids, funcs, filenames, test_cases



if __name__ == "__main__":
    batchSize = 32
    vectorDim = 40
    maxLen = 500

    # ==> 注释下面，修改
    # raw_traindataSetPath = "./dl_input/cdg_ddg/train/"
    # raw_testdataSetPath = "./dl_input/cdg_ddg/test/"
    # traindataSetPath = "./dl_input_shuffle/cdg_ddg/train/"
    # testdataSetPath = "./dl_input_shuffle/cdg_ddg/test/"
    # <==

    # ==> 添加修改
    raw_traindataSetPath = "/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/4/dl_input/train/"
    raw_testdataSetPath = "/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/4/dl_input/test/"
    traindataSetPath = "/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/4/dl_input_shuffle/train/"
    testdataSetPath = "/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/4/dl_input_shuffle/test/"
    # <==
    dealrawdata(raw_traindataSetPath, raw_testdataSetPath, traindataSetPath, testdataSetPath, batchSize, maxLen, vectorDim)
