import paramiko
import os


# def sftp_upload(host, port, username, password, local, remote):
#     sf = paramiko.Transport((host, port))
#     sf.connect(username=username, password=password)
#     sftp = paramiko.SFTPClient.from_transport(sf)
#     try:
#         if os.path.isdir(local):  # 判断本地参数是目录还是文件
#             for f in os.listdir(local):  # 遍历本地目录
#                 sftp.put(os.path.join(local + f), os.path.join(remote + f))  # 上传目录中的文件
#         else:
#             sftp.put(local, remote)  # 上传文件
#     except Exception as e:
#         print('upload exception:', e)
#     sf.close()
#
#
# def sftp_download(host, port, username, password, local, remote):
#     sf = paramiko.Transport((host, port))
#     sf.connect(username=username, password=password)
#     sftp = paramiko.SFTPClient.from_transport(sf)
#     try:
#         if os.path.isdir(local):  # 判断本地参数是目录还是文件
#             for f in sftp.listdir(remote):  # 遍历远程目录
#                 sftp.get(os.path.join(remote + f), os.path.join(local + f))  # 下载目录中文件
#         else:
#             sftp.get(remote, local)  # 下载文件
#     except Exception as e:
#         print('download exception:', e)
#     sf.close()
#
#
# if __name__ == '__main__':
#     host = '10.15.49.6'  # 主机
#     port = 22112  # 端口
#     username = 'mazhw_g'  # 用户名
#     password = '4OA9vwL'  # 密码
#     local = 'D:\\QC\YA\\0\\102109_REST2_RL.txt'  # 本地文件或目录，与远程一致
#     remote = "/public_bme/data/LTN/HCPYA_physio/102109/unprocessed/3T/rfMRI_REST2_RL/LINKED_DATA/PHYSIO/102109_3T_rfMRI_REST2_RL_Physio_log.txt" # 远程文件或目录，与本地一致，当前为linux目录格式
#
#     # sftp_upload(host, port, username, password, local, remote)  # 上传
#     sftp_download(host, port, username, password, local, remote)  # 下载

folder = os.path.exists("D:\\QC\image\\P\\")
if not folder:
    os.makedirs("D:\\QC\image\\P\\")
folder1 = os.path.exists("D:\\QC\image\\R\\")
if not folder1:
    os.makedirs("D:\\QC\image\\R\\")


client = paramiko.SSHClient()  # 获取SSHClient实例
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.15.49.6", username="mazhw_g", password="4OA9vwL", port=22112)  # 连接SSH服务端
transport = client.get_transport()  # 获取Transport实例

# 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
sftp = paramiko.SFTPClient.from_transport(transport)

# 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
# sftp.put("2021.txt", os.path.join("/home/", '2021.txt'))

# 将服务器 /www/test.py 下载到本地 aaa.py。文件下载并重命名为aaa.py
with open('D:\QC\\temp.txt', 'r') as subject_id:
    for row in subject_id:
        row = row.rstrip('\n')
        arr = row.split('/')
        url1 ='/public/home/mazhw_g/image/' + arr[10] + '_' + arr[13] + '_P' + '.png'
        # print(url)
        local1 = "D:\\QC\image\\P\\" + arr[10] + '_' + arr[13] + '_P' + ".png"
        # print(local)

        try:
            sftp.get(url1, local1)
        except Exception as e:
            print(e)
        url2 ='/public/home/mazhw_g/image/' + arr[10] + '_' + arr[13] + '_R' + '.png'
        # print(url)
        local2 = "D:\\QC\image\\R\\" + arr[10] + '_' + arr[13] + '_R' + ".png"
        # print(local)
        try:
            sftp.get(url2, local2)
        except Exception as e:
            print(e)

# 关闭连接
client.close()