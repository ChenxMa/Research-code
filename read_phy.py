import pandas as pd
import sys
import os
dir_path = "/hpc/data/home/bme/mazhw/group/DICOM/2022/"
home_path = "/public/home/mazhw_g/v-machx1/UI_Physio/"
for root, dirs, files in os.walk(dir_path):
    for name in files:
        file_path = home_path + root.split('/')[7:]
        print(file_path)
        if name[-5:]=="pulse":
            df = pd.read_table(os.path.join(root,name), delimiter=';',  names=['Time','Data']) #将数据根据;切片成Time与Data
            for i in range(0,len(df)):
                df.Data[i] = df.Data[i].split('|')[0][6:] #选择Data列数据，只保留数据部分，并以|为界限除去Trigger
            print(df.Data)
            df.Data.to_csv(file_path + "/pulse.csv")
        if name[-4:]=="resp":
            df = pd.read_table(os.path.join(root, name), delimiter=';', names=['Time', 'Data'])
            for i in range(0, len(df)):
                df.Data[i] = df.Data[i].split('|')[0][6:]
            print(df.Data)
            df.Data.to_csv(file_path + "/resp.csv")
        if name[-4:]=="mmwr":
            df = pd.read_table(os.path.join(root, name), delimiter=';', names=['Time', 'Data'])
            for i in range(0, len(df)):
                df.Data[i] = df.Data[i].split('|')[0][6:]
            print(df.Data)
            df.Data.to_csv(file_path + "/mmwr.csv")