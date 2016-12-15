import sys
import pandas as pd
import os
import numpy as np
from scipy.sparse import csr_matrix

from scipy.sparse import lil_matrix
from sklearn.feature_extraction.text import CountVectorizer


#np.exp(np.sum(np.log(np.power(w_post[j,:], tfdf[i, :].toarray()[0]))))

def merge(directory, out_name):
    sum = 0
    files = [x for x in os.listdir(directory) if '.' in x and 'Symptom_vec' in x ]
    files = [x for x in files if x.split('.')[1] == 'pickle']
    print files

    root_p = pd.read_pickle(directory + files[0])
    sum = sum + root_p.shape[0]
    print files[0]
    root= [root_p[x] for x in range(root_p.shape[0])]

    for file in files[1:]:
        print file
        tmp = pd.read_pickle(directory + file)
        sum = sum + tmp.shape[0]
        if len(tmp.shape) == 1:
            for x in range(tmp.shape[0]):
                if isinstance(tmp[x], pd.Series):
                    root.append(tmp[x])

    if '.pickle' in out_name:
        pd.to_pickle(pd.Series(root), out_name)
    else:
        pd.to_pickle(pd.Series(root), out_name + '.pickle')

    print sum
    return pd.Series(root)



def tf_df(df, out_name):


    print "Creating TF_IDF Matrix"
    unique_words = set()
    for x in range(df.shape[0]):
        for y in list(df.ix[x].index):
            unique_words.add(y)

    print "TFDF: Creating TF IDF"
    # tf_matrix = np.zeros((df.shape[0], len(unique_words)))
    tf_matrix = lil_matrix((df.shape[0], len(unique_words)))
    for i in range(df.shape[0]):
        print "Iteration {} out of {}".format(i, df.shape[0])
        for j, word in enumerate(unique_words):
            #print "Iteration (%d, %d) out of (%d, %d)" % (i, j, df.shape[0], len(unique_words))
            complaint_words = list(df.ix[i].index)
            if word in complaint_words:
                index = complaint_words.index(word)
                tf_matrix[i, j] = df.ix[i][index]

    tf_df = pd.DataFrame(tf_matrix.todense(), index=range(tf_matrix.shape[0]), columns=list(unique_words))

    if '.pickle' in out_name:
        pd.to_pickle(tf_df, out_name)
    else:
        pd.to_pickle(tf_df + '.pickle', out_name)

    return tf_df



def test(df):
    cv = CountVectorizer(stop_words=None, min_df=0, lowercase=False,token_pattern=r"\b\w+\b")
    words = []
    for x in range(df.shape[0]):
        words.append(' '.join([(df.ix[x].index[i] + ' ')*df.ix[x][i] for i in range(len(df.ix[x]))] ))

    tfmatrix = cv.fit_transform(words)
    vocab = cv.get_feature_names()



    return tfmatrix , vocab, words, cv


#tfmatrix[0,tfmatrix[0,:].nonzero()[1]].toarray()[0]


def main():
    # print sys.argv
    # directories = sys.argv[1:]
    directories = [os.getcwd() + '/pickles/']
    print directories
    for directory in directories:
        big_pickle =  merge(directory, 'Big_Pickle.pickle')

    #tfdf =  tf_df(big_pickle, 'TFDF_Matrix.pickle')






if __name__ == '__main__':
    main()
