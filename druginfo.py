import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import numpy as np
import re
from datasketch import MinHash, MinHashLSHForest


df = pd.read_csv("C:/Users/samee/Downloads/drugLib_raw/drugLibTest_raw.tsv", delimiter='\t')
df2 = pd.read_csv("C:/Users/samee/Downloads/drugLib_raw/drugLibTrain_raw.tsv", delimiter='\t')

df.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","effectiveness","sideEffects"], axis=1,inplace=True)
df2.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","effectiveness","sideEffects"], axis=1,inplace=True)

#print(df.isna())
df = pd.concat([df, df2], ignore_index=True)
#print(df)
#%matplotlib inline
#fig = plt.figure()
#print(fig)
#print(df.index)
#msno.matrix(df)
#fig = plt.figure()
#fig.savefig(a)

df = df.dropna()
#print(df.dropna())

df = df.dropna().reset_index()
df.drop(['index'], axis=1,inplace=True)
#print(df)

def preprocess(text):
    #text = re.sub('-',' ',text)
    text = text.lower()
    tokens = set()
    for i in range(0,len(text) - 2):
        shingle = text[i] + text[i+1] + text[i+2]
        tokens.add(shingle)
    #tokens = text.split()
    #tokens = list(text)
    return tokens

#print(preprocess(df.at[9,'urlDrugName']))
#print(df.index)
m = []
for index in df.index:
    t = preprocess(df.at[index, 'urlDrugName'])
    mh = MinHash(num_perm=256)
    #tlist = str(t)
    #print(tlist)
    for d in t:
        #print(d)
        mh.update(d.encode('utf8'))
        #print(mh)
    m.append(mh)
    del mh

#print(m)
#actual_jaccard = float(len(m[14].intersection(m[22])))/float(len(m[14].union(m[22])))
print(df.index)
print(df.at[14, 'urlDrugName'])
print(df.at[22, 'urlDrugName'])
print(len(df.at[14, 'urlDrugName']))
print(len(df.at[22, 'urlDrugName']))
print(m[14].jaccard(m[22]))
#print(actual_jaccard)


lsh = MinHashLSH(threshold=0.95, num_perm=256)
for minh in range(0, len(m)):

    lsh.insert(df.at[minh, 'urlDrugName'],m[minh])
result = lsh.query(m[1])
print(result)
