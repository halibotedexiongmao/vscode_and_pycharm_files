import requests
#head={"User-Agent":"Mozilla/5.0"} #等等，没搞清楚
response=requests.get("http://books.toscrape.com/")
if response.ok:
    print(response.text)
else:
    print("请求失败")