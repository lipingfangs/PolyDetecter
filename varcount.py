import sys
import re
import os

mygodir = sys.argv[1]

listdir = os.listdir(mygodir)


for i in listdir:
    filerun = open(mygodir+"/"+i,"r")
    filerunline = filerun.readlines()
    filerun.close()
    dic = {}
    for k in filerunline:
        k = k.strip()
        k = k.split("\t")
        #print(k,k[3:])
        cnumber = int(k[1].split(":")[1])
        varj = ""
        for j in k[3:]:
            jv = j.split()
            pos = int(jv[0])
            if 24 < pos< 106:
                varj = varj + j+" " 
                
        if varj not in dic.keys():
            dic[varj] = 0
            dic[varj] += cnumber
        else:
            dic[varj] += cnumber   
        
    for k in dic.keys():
        print(i,dic[k],k,sep = "\t")
