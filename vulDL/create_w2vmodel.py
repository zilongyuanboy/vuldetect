## coding: utf-8
'''
This python file is used to tranfer the words in corpus to vector, and save the word2vec model under the path 'w2v_model'.
'''

from gensim.models.word2vec import Word2Vec   # gensim == 3.4
import pickle
import os
import gc

'''
DirofCorpus class
-----------------------------
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
                print(fn)
                # ==> 这里要做个文件判断，可能取出的fn不是文件夹
                if not os.path.isdir(os.path.join(d, fn)):  # ==> 自己添加一行代码
                    continue
                for filename in os.listdir(os.path.join(d, fn)):
                    samples = pickle.load(open(os.path.join(d, fn, filename), 'rb'))[0]
                    for sample in samples:
                        yield sample
                    del samples
                    gc.collect()

'''
generate_w2vmodel function
-----------------------------
This function is used to learning vectors from corpus, and save the model

# Arguments
    decTokenFlawPath: String type, the src of corpus file 
    w2vModelPath: String type, the src of model file 
    
'''

def generate_w2vModel(decTokenFlawPath, w2vModelPath):
    print("training...")
    model = Word2Vec(sentences= DirofCorpus(decTokenFlawPath), size=30, alpha=0.01, window=5, min_count=0, max_vocab_size=None, sample=0.001, seed=1, workers=1, min_alpha=0.0001, sg=1, hs=0, negative=10, iter=5)
    # model.save(w2vModelPath)  # ==> 注意这里的保存路径不能是一个文件夹，即前面提供路径的时候最后一层就不要手动创建文件夹了，wordmodel3就是文件夹, wordmodel.h5 是文件名
    model.save(w2vModelPath)

def evaluate_w2vModel(w2vModelPath):
    print("\nevaluating...")
    model = Word2Vec.load(w2vModelPath)
    for sign in ['(', '+', '-', '*', 'main']:
        # ==> 在测试的时候有可能出现字符不全的情况，即上诉字符不包括在训练词汇中，故做个过滤
        if sign not in model.wv.index2word:
            continue
        # <==
        print(sign, ":")
        print(model.most_similar_cosmul(positive=[sign], topn=10))
    
def main():
    # ==>
    # dec_tokenFlaw_path = ['./data/cdg_ddg/corpus/']
    # w2v_model_path = "./w2v_model/wordmodel3"
    # <== 注释上面，添加下面
    dec_tokenFlaw_path = ['/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/4/corpus/']
    w2v_model_path = "/Users/zilong/SySeVR/self_Implementation/Implementation/source2slice/C/test_data/w2v_model/wordmodel3/wordmodel.h5"

    generate_w2vModel(dec_tokenFlaw_path, w2v_model_path)
    evaluate_w2vModel(w2v_model_path)
    print("success!")
 
if __name__ == "__main__":
    main()


