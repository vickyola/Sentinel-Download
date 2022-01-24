# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 15:09:20 2022

@author: wittekii
"""
import os
from os import walk
import pandas as pd
mypath = os.getenv('PATHIN')
out_path = os.getenv('PATHOUT')
f = list()
for (dirpath, dirnames, filenames) in walk(mypath):
    f.append(dirnames)
    break

df = pd.DataFrame(f)
df= df.T
df.to_excel(out_path)

print(df)
