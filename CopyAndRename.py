import shutil
import os

with open("/public/home/mazhw_g/filelist.txt") as file_read:#使用ls -a>~/filelist.txt 读取所有受试者名称

    for row in file_read:#逐行读取受试者的名称
        row = row.rstrip('\n')#除去文件后的\n
        src = "/public_bme/data/LTN/UKB/T1/" + row + "/T1/T1_unbiased_brain.nii.gz"# 目标路径
        dst = "/public_bme/data/LTN/UKB/T1_temp/" + row + "_T1_unbiased_brain.nii.gz"# 目标路径+文件重命名
        if os.path.exists(src):#判断文件是否存在
            shutil.copy(src, dst)#开始复制

        