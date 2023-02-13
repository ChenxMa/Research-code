import pandas as pd
import sys
import os
dir_path =  "/hpc/data/home/bme/mazhw/group/DICOM/2022/"
home_path = "/public/home/mazhw_g/v-machx1/UI_Physio/"
for root, dirs, files in os.walk(dir_path):
    for name in files:
        file_path = home_path + root[len(dir_path):]
        if name[-9:]=="pulse.dat":
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            df = pd.read_table(os.path.join(root, name), delimiter=',', names=['TimeStamp', 'WaveData', 'Trigger'],
                               skiprows=[0, 1, 2, 3, 4, 5, 6])
            print(df)
            file_name = name.split(".")[0].split("_",2)[2] #抹去UID，保留scan信息
            csv_name = file_path + "/" +file_name + "_pulse.csv"
            df.to_csv(csv_name)
        if name[-8:]=="resp.dat":
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            df = pd.read_table(os.path.join(root, name), delimiter=',', names=['TimeStamp', 'WaveData', 'Trigger'],
                               skiprows=[0, 1, 2, 3, 4, 5, 6])
            print(df)
            file_name = name.split(".")[0].split("_",2)[2]
            csv_name = file_path + "/" + file_name + "_resp.csv"
            df.to_csv(csv_name)
        if name[-8:]=="mmwr.dat":
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            df = pd.read_table(os.path.join(root, name), delimiter=',', names=['TimeStamp', 'WaveData', 'Trigger'],
                               skiprows=[0, 1, 2, 3, 4, 5, 6])
            print(df)
            file_name = name.split(".")[0].split("_",2)[2]
            csv_name = file_path + "/" + file_name + "_mmwr.csv"
            df.to_csv(csv_name)