import webbrowser
import pyperclip

while True:
    #input_file = pyperclip.paste().split("\n")
    input_file = input("企业名称：")
    company_list = input_file.split(" ")#粘贴进去的内容不要带有回车换行符，不然会运行失败，用空格隔开
    url_list=[]
    for company in company_list:
        if company!= "":
            url = "https://cn.bing.com/search?pglt=129&q=" + company
            url_list.append(url)
            
    for url in url_list:
        webbrowser.register('msedge', None, webbrowser.BackgroundBrowser('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'))
        webbrowser.get('msedge').open(url)