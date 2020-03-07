# -*- coding: utf-8 -*-

"""
Author: Noah Becker
Date: February 17th, 2020
Subject: Causal Inference
Description: Analysis
"""

import numpy as np
import pandas as pd

df = pd.read_csv('swim.csv')

df = df.dropna(subset=['Lane'])

# https://stackoverflow.com/questions/28845825/pandas-python-convert-hhmmss-into-seconds-in-aggegate-csv-file
def time_convert(x):
    if ':' not in x:
        m = 0
        s = float(x)
    else:
        m, s = map(float, x.split(':'))
    return (m * 60) + s

df['Prelims Time'] = df['Prelims Time'].apply(time_convert)
df['Finals Time'] = df['Finals Time'].apply(time_convert)

df = df.drop(columns = ['Swimmer', 'Distance', 'Lanes', 'School', 'Seed Time',
                        'Prelims Lane', 'Finals Lane', 'Prelims Heat', 
                        'Finals Heat', 'Prelims Pl', 'Finals Pl', 'Pts'])

df = df.rename(columns = {'Finals Time':'FinalsTime', 'Prelims Time':'PrelimsTime'})
    

df.to_csv('clean.csv', index = False)
