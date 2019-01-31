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
