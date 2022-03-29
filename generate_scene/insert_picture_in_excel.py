"""
adapt the genereate excel file of the scenes to take into account the acquired images paths
"""
import os, glob, csv, openpyxl
import pandas as pd

os.chdir(r"path")

list_files = glob.glob("*")

list_files = list_files[1::4]               # for 4 cameras network
for i, file in enumerate(list_files):
    file = file.split("_cam")[0]
    list_files[i] = file

lights_on = list_files[0::2]                # with/without lights
lights_off = list_files[1::2]

os.chdir(r"path")

df = pd.read_excel('your_excel.xlsx')
a = [df.loc[i,["file"]][0] for i in range(df.shape[0])] #select correct column
index = next((i for i, x in enumerate(a) if x==0), None)

nf = df.to_numpy()
nf[:,15] = a[:index] + lights_on + (df.shape[0]-len(lights_on)-index)*[0] #column for pictures with lights on
nf[:,16] = index*[0] + lights_off + (df.shape[0]-len(lights_on)-index)*[0] #for lights off

pf = pd.DataFrame(data = nf, columns = df.columns)
pf.to_excel('your_excel.xlsx')
