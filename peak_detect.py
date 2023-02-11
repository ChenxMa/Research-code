
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from detecta import detect_peaks
import sys

# x = np.random.randn(100)
# x[60:81] = np.nan
# # detect all peaks and plot data
# ind = detect_peaks(x, show=True)
# print(ind)

# x = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 200)) + np.random.randn(200) / 5
# # set minimum peak height = 0 and minimum peak distance = 20
# detect_peaks(x, mph=None, mpd=20, show=True, threshold=1)

#  x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
#   # set minimum peak distance = 2
# detect_peaks(x, mpd=1, show=True)

# x = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 200)) + np.random.randn(200) / 5
#  # detection of valleys instead of peaks
# detect_peaks(x, mph=-1.2, mpd=20, valley=True, show=True)

# x = [0, 1, 1, 0, 1, 1, 0]
#  # detect both edges
# detect_peaks(x, edge='rising', show=True)
#
# x = [-2, 1, -2, 2, 1, 1, 3, 0, 2 , 0, 3, 2]
#   # set threshold = 2
# detect_peaks(x, threshold=2, show=True)

# x = [-2, 1, -2, 2, 1, 1, 3, 0]
# # fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(10, 4))
# detect_peaks(x, threshold=0.5, title=False, show=True)
# detect_peaks(x, threshold=1.0, title=False, show=True)
#


input_file = sys.argv[1]  # 由于sys.argv[]下标是从0开始的，所以sys.argv[1]捕获到的是第二个参数，也就是txt文本文件

file_read = open(input_file, 'r') #只读模式操作文本文件

for row in file_read:
    # print(row.strip())


    data=pd.read_csv(row.strip(),
                     usecols=["RESP","PULS"], na_values="0")# 读入RESP、PULS数据，过程中将零点置为空值NA

    data=data.dropna() # 去除空值

    data_R=data.RESP # 取RESP列数据
    data_P=data.PULS # 取PULS列数据


    a_data_R=np.array(data_R) # 将dataframe格式转为arry格式
    a_data_R=a_data_R.flatten() # 将二维数组转为一维数组
    a_data_P=np.array(data_P) # 将dataframe格式转为arry格式
    a_data_P=a_data_P.flatten() # 将二维数组转为一维数组
    detect_peaks(a_data_R, mpd=1, mph=4000, show=True, threshold=0)  # 检查处理前数据
    detect_peaks(a_data_P, mpd=1, mph=3800, show=True, threshold=0)  # 检查处理前数据

    for i in range(0,200):
        ind1 = detect_peaks(a_data_R, mpd=1, mph=4000, show=False, threshold=0, edge='both')  # 检查上升沿峰值
        ind2 = detect_peaks(a_data_R, mpd=1, mph=1000, valley=True, show=False, edge='both')  # 检查下降沿峰值
        ind = np.concatenate((ind1, ind2), axis=0)  # 将两组数据拼接
        a_data_R = np.delete(a_data_R, ind)  # 根据索引删除数据
        a_data_P = np.delete(a_data_P, ind)  # 根据索引删除数据

        ind1 = detect_peaks(a_data_P, mpd=8, mph=3800, show=False, threshold=0, edge='both')  # 检查上升沿峰值
        ind2 = detect_peaks(a_data_P, mpd=8, mph=500, valley=True, show=False, edge='both')  # 检查下降沿峰值
        ind = np.concatenate((ind1, ind2), axis=0)  # 将两组数据拼接
        a_data_R = np.delete(a_data_R, ind)  # 根据索引删除数据
        a_data_P = np.delete(a_data_P, ind)  # 根据索引删除数据


    detect_peaks(a_data_R, mpd=1, mph=4000, show=True, threshold=0)  # 检查处理后数据
    detect_peaks(a_data_P, mpd=1, mph=3800, show=True, threshold=0)  # 检查处理后数据


    data_R=pd.DataFrame(a_data_R)  # 转为dataframe格式
    data_P=pd.DataFrame(a_data_P)  # 转为dataframe格式
    data=pd.concat([data_R, data_P], axis=1)  # 合并
    new_col=['RESP', 'PULS']
    data.columns=new_col  # 设置列名称
    print(data)  # 查看剩余数据长度
    processed=row.strip()+'_processed'
#    data.to_csv(processed + '.csv', index= 0)
file_read.close()




