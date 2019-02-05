import pandas as pd
#import missingno as msno
#import matplotlib.pyplot as plt
import numpy as np
#import re
from datasketch import MinHash, MinHashLSH, MinHashLSHForest
import os
import boto3

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')

bucket_name = "drug-data"
file_name_1 = "drugLibTest_raw.tsv"
file_name_2 = "drugLibTrain_raw.tsv"
session = boto3.Session(aws_access_key, 
		aws_secret_access_key)

s3 = session.resource('s3')

#bucket = conn.get_bucket(bucket_name)
#key_1 = bucket.get_key(file_name_1)
#key_2 = bucket.get_key(file_name_2)

#data_1 = key_1.get_contents_as_string()
#data_2 = key_2.get_contents_as_string()
data_loc1 = 's3://{}/{}'.format(bucket_name, file_name_1)
data_loc2 = 's3://{}/{}'.format(bucket_name, file_name_2)

df = pd.read_csv(data_loc1, delimiter='\t')
df2 = pd.read_csv(data_loc2, delimiter='\t')

df.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","sideEffects"], axis=1,inplace=True)
df2.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","sideEffects"], axis=1,inplace=True)

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

# ultram-er
# ultram-xr

df = df.dropna().reset_index()
df.drop(['index'], axis=1,inplace=True)
#df = df.reset_index()
print(df)

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
#print(df.index)
#print(df.at[14, 'urlDrugName'])
#print(df.at[22, 'urlDrugName'])
#print(len(df.at[14, 'urlDrugName']))
#print(len(df.at[22, 'urlDrugName']))
#print(m[14].jaccard(m[22]))
#print(actual_jaccard)

'''
lsh = MinHashLSH(threshold=0.95, num_perm=256)
for minh in range(0, len(m)):
    #print(minh)
    if df.at[minh,'urlDrugName'] not in lsh:
        lsh.insert(df.at[minh, 'urlDrugName'],m[minh])

result = lsh.query(m[14])
print(result)
print(len(lsh))
'''

sub = '-'
#print(len([s for s in df['urlDrugName'] if sub in s]))
'''
hyphen = [s for s in df['urlDrugName'] if sub in s]
print(df.query('-' in 'urlDrugName').index)
print(hyphen)
print(df.xs('urlDrugName','index'))
print(df[['urlDrugName']])
hyphen = df[['urlDrugName']]
'''

for i in range(0, len(df.index)):
    for j in range(i, len(df.index)):
        if m[i].jaccard(m[j]) >= 0.25 and df.at[i, 'urlDrugName'] != df.at[j, 'urlDrugName']:
            if len(df.at[i, 'urlDrugName']) > len(df.at[j, 'urlDrugName']):
                if df.at[j, 'urlDrugName'] in df.at[i, 'urlDrugName']:
                    #print("changed name i " + df.at[i, 'urlDrugName'], df.at[j, 'urlDrugName'])
                    df.at[i, 'urlDrugName'] = df.at[j, 'urlDrugName']
            elif len(df.at[j, 'urlDrugName']) > len(df.at[i, 'urlDrugName']):
                if df.at[i, 'urlDrugName'] in df.at[j, 'urlDrugName']:
                    #print("changed name j " + df.at[j, 'urlDrugName'], df.at[i, 'urlDrugName'])
                    df.at[j, 'urlDrugName'] = df.at[i, 'urlDrugName']
            #else:
             #   print(df.at[i, 'urlDrugName'], df.at[j, 'urlDrugName'])

print(df)
#print(len([s for s in df['urlDrugName'] if sub in s]))
#print([s for s in df['urlDrugName'] if sub in s])

'''
hyphen = df[['urlDrugName']]
for s in hyphen.index:
        if sub in df.at[s, 'urlDrugName']:
            hyphen.drop([s])

print(hyphen)'''
'''print(m[df.index[df['urlDrugName'] == 'xanax'][0]].jaccard(m[df.index[df['urlDrugName']][0]]))

for s in df['urlDrugName']:
    if sub in s:
        for t in df['urlDrugName']:
            if m[df.index[df['urlDrugName'] == s]].jaccard(m[df.index[df['urlDrugName'] == t]]) in range(0.9,1.0):
                print("yay")

print('done') '''
