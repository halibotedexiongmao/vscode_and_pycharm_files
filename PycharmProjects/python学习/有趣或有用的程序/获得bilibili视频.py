'''import requests
url = "https://www.bilibili.com/video/BV1mf4y157ZU/?spm_id_from=333.1391.0.0&vd_source=5dce81b8e2b3411265d9bd4a76eaac59"  # 替换为实际文件链接
response = requests.get(url, stream=True)
if response.status_code == 200:
    # 继续下载
else:
    print(f"下载失败，状态码：{response.status_code}")'''
import subprocess