# dir =['REST1_AP', 'REST1_PA', 'REST2_AP', 'REST2_PA']
# with open('D:\\QC\\name.txt', 'w') as f:
#     for content in range(1, 725):
#         for i in range(0, len(dir)):
#             f.write(dir[i] + '\n')

with open('D:\QC\list.txt', 'r') as l:
    for line in l:
        for i in range(1,3):
            line = line + line
        with open('D:\QC\list_new.txt', 'a') as f:
            for j in range(1, 2):
                f.write(line)


