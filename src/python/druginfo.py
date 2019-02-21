import os

import boto3
import MySQLdb
import sqlalchemy
import numpy as np
import pandas as pd
from datasketch import MinHash
from six.moves import configparser


def create_df(data_location_1, data_location_2):
    df1 = pd.read_csv(data_loc1, delimiter='\t')
    df2 = pd.read_csv(data_loc2, delimiter='\t')

    df1.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","sideEffects"], axis=1,inplace=True)
    df2.drop(["Unnamed: 0","benefitsReview","sideEffectsReview","commentsReview","sideEffects"], axis=1,inplace=True)

    df = pd.concat([df1, df2], ignore_index=True)

    df = df.dropna().reset_index()
    df.drop(['index'], axis=1,inplace=True)
    return df

def create_shingles(text):
    text = text.lower()
    tokens = set()
    for i in range(0,len(text) - 2):
        shingle = text[i] + text[i+1] + text[i+2]
        tokens.add(shingle)
    return tokens

def hashing():
    m = []
    for index in df.index:
        t = create_shingles(df.at[index, 'urlDrugName'])
        mh = MinHash(num_perm=256)
        for d in t:
            mh.update(d.encode('utf8'))
        m.append(mh)
        del mh
    return m

def preprocess():
    minhash = hashing()
    for i in range(0, len(df.index)):
        for j in range(i, len(df.index)):
            if minhash[i].jaccard(minhash[j]) >= 0.25 and df.at[i, 'urlDrugName'] != df.at[j, 'urlDrugName']:
                if len(df.at[i, 'urlDrugName']) > len(df.at[j, 'urlDrugName']):
                    if df.at[j, 'urlDrugName'] in df.at[i, 'urlDrugName']:
                        df.at[i, 'urlDrugName'] = df.at[j, 'urlDrugName']
                elif len(df.at[j, 'urlDrugName']) > len(df.at[i, 'urlDrugName']):
                    if df.at[i, 'urlDrugName'] in df.at[j, 'urlDrugName']:
                        df.at[j, 'urlDrugName'] = df.at[i, 'urlDrugName']

    df.columns = ['name', 'rating', 'effectiveness','diagnosis']

def mysqlconnect():

    config = configparser.ConfigParser()

    config.read('config.ini')
    dbname = config.get('auth', 'dbname')
    dbuser = config.get('auth', 'user')
    dbpass = config.get('auth', 'password')
    dbhost = config.get('auth', 'host')
    dbport = config.get('auth', 'port')

    try:
        db_conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbname)
        print("Connected")
    except Exception as e:
        print(e)

    cursor = db_conn.cursor()

    try:
        sql = "CREATE TABLE IF NOT EXISTS druginfo(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), rating INT, effectiveness VARCHAR(255), diagnosis VARCHAR(255))"
        cursor.execute(sql)
        print("Created table")
    except Exception as e:
	    print(e)

    try:
    	df.to_sql(name = 'druginfo', con=db_conn, if_exists='append', flavor='mysql', index=False)
        print("Inserted dataframe into table")
    except Exception as e:
	    print(e)

    db_conn.commit()
    db_conn.close()
   
if __name__ == "__main__":
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')
    session = boto3.Session(aws_access_key, aws_secret_access_key)
    s3 = session.resource('s3')

    bucket_name = "drug-data"
    file_name_1 = "drugLibTest_raw.tsv"
    file_name_2 = "drugLibTrain_raw.tsv"

    data_loc1 = 's3://{}/{}'.format(bucket_name, file_name_1)
    data_loc2 = 's3://{}/{}'.format(bucket_name, file_name_2)

    df = create_df(data_loc1, data_loc2)
    preprocess()
    mysqlconnect()
