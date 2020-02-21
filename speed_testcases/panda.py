import pandas as pd
import numpy as np
#import time

def read_file():
    df = pd.read_csv("flp.csv",lineterminator="\n")

    #print(df)
    return df

def calculations_pandas(df):
    #df['Sum']= df.apply(lambda x : x.X + x.Y , axis=1)
    df['Sum']= df['X']+df['Y']
    return df

def calculations_numpy(df):
    arrX = df['X'].values
    arrY = df['Y'].values
    arrSum = arrX + arrY
    return arrSum

#print("Hello")
df = read_file()
#start_pd = time.start()
df=calculations_pandas(df)
#end_pd = time.start()

arrSum=calculations_numpy(df)

#print(df.shape)
#print(arrSum.shape)
