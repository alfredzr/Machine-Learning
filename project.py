# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 03:28:12 2018

@author: Alfred Zane Rajan
"""
import sys
from statistics import stdev as sd
from statistics import mean as mean

print("Reading data")

data = "traindata/traindata"
#data = sys.argv[1]
IN = open(data)
datac = list()
line = IN.readline()
a = line.split()
for j in range(len(a)):
    datac.append(list())
    datac[j].append(int(a[j]))
line = IN.readline()
while line != '':
    a = line.split()
    for j in range(0, len(a), 1):
        datac[j].append(int(a[j]))
    line = IN.readline()
IN.close()

rows = len(datac)
cols = len(datac[0])

print("Reading Labels")
data2 = "trainlabels.txt"
#data2 = sys.argv[2]
IN = open(data2)
labels = {}
line = IN.readline()
while line != '':
    a = line.split()
    labels[int(a[1])] = int(a[0])
    line = IN.readline()
labels = [labels[i] for i in labels]

def Chi2(x, y):
    cols = len(x)
    rows = len(x[0])
    chi2 = []
    for j in range(0, cols):
        ct = [[1,1],[1,1],[1,1]]
        dtotal = [2,2,2]
        ltotal = [3,3]
        total = 6
        for i in range(0, rows):
            ct[ x[j][i] ] [ y[i] ] += 1
            dtotal[x[j][i]] += 1
            ltotal[y[i]] += 1
            total+=1
        exp_value = [[(row*col)/total for row in ltotal] for col in dtotal]
        sqr_value = [[((ct[i][j] - exp_value[i][j])**2)/exp_value[i][j] for j in range(2)] for i in range(3)]
        chi = sum([sum(s) for s in sqr_value])
        chi2.append(chi)
        print( "Column:", j, "Chi:", chi)
    return chi2

def pearson ( x, y):
    p = [x[i]*y[i] for i in range(len(y))]
    if sd(x) != 0:        
        return(
                ( mean(p) - mean(x)*mean(y) ) / ( sd(x)* sd(y) )
                )
    else:
        return( 0.0)

print("Getting correlations")

p = Chi2( datac, labels)

print("Selecting best rows without redundancy")
highp = []
for j in range(len(p)):
    if int(p[j]) > 80:
        highp.append(j)
redund = []
for a in range(len(highp)-1):
    for b in range(a+1,len(highp),1):
        tmp = pearson( datac[highp[a]], datac[highp[b]])
        if abs(tmp) > 0.7:
            if p[highp[a]] < p[highp[b]]:
                if highp[a] not in redund:
                    redund.append(highp[a])
            else:
                if highp[b] not in redund:
                    redund.append(highp[b])

final = []
for i in highp:
    if i not in redund:
        final.append(i)

fdatac = [datac[i] for i in final]

fdata = []
for i in range(len(fdatac[0])):
    row = []
    for j in range(len(fdatac)):
        row.append(fdatac[j][i])
    fdata.append(row)


data3 = "testdata/testdata"
#data3 = sys.argv[3]
IN = open(data3)
ftest = list()
line = IN.readline()
while line != '':
    l = list()
    a = line.split()
    for j in range(0, len(a), 1):
        if j in final:
            l.append(int(a[j]))
    ftest.append(l)
    line = IN.readline()
IN.close()

print("Training model")
from sklearn.svm import SVC  
svclassifier2 = SVC(kernel='linear')  
svclassifier2.fit(fdata, labels)
print("Predictions:")
prediction = svclassifier2.predict(ftest)
prediction = list(prediction)

for i in range(len(prediction)):
    print(prediction[i], i)

print("Features used = ", len(final), ":")
for i in final:
    print(i)