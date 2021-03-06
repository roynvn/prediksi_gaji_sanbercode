# -*- coding: utf-8 -*-
"""Prediksi Gaji.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H_nhqDf6i2t_JHB6IHAOmbi4XHdJUYlp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix, accuracy_score, f1_score, make_scorer
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import train_test_split



#buat dataframe untuk train dan test
df_train = pd.read_csv("train.csv")
df_val = pd.read_csv("test.csv")

df_train

df_val

#cek data kosong
print("DATA TRAIN")
df_train.isnull().sum()

print("DATA VALIDATION")
df_val.isnull().sum()

#cek missing value pada kolom prakerja
df_train['Kelas Pekerja'].value_counts()

df_val['Kelas Pekerja'].value_counts()

df_train['Pekerjaan'].value_counts()

df_val['Pekerjaan'].value_counts()

#ubah value ? pada setiap nilai dan tambahkan ke modus 
#kolom kelas pekerja
df_train['Kelas Pekerja'] = df_train['Kelas Pekerja'].replace(['?'],"Wiraswasta")
df_val['Kelas Pekerja'] = df_val['Kelas Pekerja'].replace(['?'],"Wiraswasta")
#kolom pekerjaan
df_train['Pekerjaan'] = df_train['Pekerjaan'].replace(['?'],"Spesialis")
df_val['Pekerjaan'] = df_val['Pekerjaan'].replace(['?'],'Perbaikan Kerajinan')

'''ubah nilai gaji menjadi data kategorikal dengan ketentuan:
   <= 7jt = 0,
   > 7 jt = 1
'''
df_train['Gaji'] = df_train['Gaji'].replace(['<=7jt','>7jt'],[0,1])

#ubah data nilai pendidikan ke menjadi int
df_train['Pendidikan'].value_counts()
obj_dict={
    '1st-4th'              : 0,
    '5th-6th'              : 1,
    'SD'                   : 2,  
    '7th-8th'              : 3,   
    '9th'                  : 4,
    '10th'                 : 5,
    '11th'                 : 6, 
    '12th'                 : 7,
    'SMA'                  : 8,                 
    'Sekolah Professional' : 9,
    'D3'                   : 10,                      
    'D4'                   : 11,
    'Pendidikan Tinggi'    : 12,  
    'Sarjana'              : 13,
    'Master'               : 14,
    'Doktor'               : 15
}

#one hot encoding 
df_dummy_train = pd.get_dummies(df_train, columns=['Kelas Pekerja','Status Perkawinan','Pekerjaan','Jenis Kelamin'])
df_dummy_train['Pendidikan'] = df_dummy_train['Pendidikan'].replace(obj_dict)
df_dummy_train

df_dummy_val = pd.get_dummies(df_val, columns=['Kelas Pekerja','Status Perkawinan','Pekerjaan', 'Jenis Kelamin'])
df_dummy_val['Pendidikan'] = df_dummy_val['Pendidikan'].replace(obj_dict)
df_dummy_val

#split data feature dan target
X = df_dummy_train.drop(['id','Gaji'],axis=1)
y = df_dummy_train['Gaji']
X_val = df_dummy_val.drop('id',axis=1)

#normalisasi
col_train         = X.columns
col_val           = X_val.columns
stdscalar         = StandardScaler()
data_scale_train  = stdscalar.fit_transform(X)
data_scale_val   = stdscalar.fit_transform(X_val)

data_train = pd.DataFrame(data_scale_train, columns=col_train)
data_val = pd.DataFrame(data_scale_val, columns=col_val)

#training model
X_train, X_result, y_train, y_result = train_test_split(data_train, y, test_size=0.2, random_state=0)
model = DecisionTreeClassifier()
param_grid = {'criterion': ['gini', 'entropy'],
              'splitter': ['best', 'random'],
              'max_features': ['auto', 'sqrt', 'log2'],
              'max_depth': np.arange(1,30),
              'min_samples_leaf' : np.arange(1,5)
             }
rscv = RandomizedSearchCV(model, param_grid, scoring='roc_auc', cv=10)
rscv.fit(X_train,y_train)

rscv.best_params_

rscv.best_score_

rscv.classes_

"""CONFUSION MATRIX MODEL"""

y_predict = rscv.predict(X_result)
print(confusion_matrix(y_result,y_predict))
print(classification_report(y_result,y_predict))
print('nilai akurasinya adalah ',accuracy_score(y_result, y_predict))

"""IMPLEMENTASI TERHADAP DATA VALIDATION"""

prediksi = rscv.predict_proba(X_val)
prediksi