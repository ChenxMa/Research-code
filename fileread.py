import os,zipfile
file_dir="D:\\test\\temp\\5480581_20227_2_0"
file_name="D:\\test\\temp\\5480581_20227_2_0.zip"

with zipfile.ZipFile(file_name, 'r') as z:  # 解压
    filelist = []
    for root, dirs, files in os.walk(file_dir):
        for name in files:
            fullname = os.path.join(root, name)
            clipname = fullname[31:]
            clipname = clipname.replace("\\","/")
            filelist.append(clipname)
    print(list(set(z.namelist()).difference(set(filelist))))


