import requests
import re
from bs4 import BeautifulSoup


def get_report_url(stock_code):
    
    
    
    url = f'https://q.stock.sohu.com/cn/{stock_code}/cwbg.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    print(f'查询股票{stock_code}')
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    if response.status_code!= 200:
        print("获取链接失败")
        
    soup = BeautifulSoup(response.text, 'html.parser')
        # 查找包含“2023年年度报告”的链接
    report_links = []
    
    biz_inner_content_div = soup.find('div', class_='BIZ_innerContent').find('ul')
    for link in biz_inner_content_div.find_all('a', href=True):
        if "2023年年度报告" in link.text:
            if '摘要' in link.text:
                continue
            report_links.append(link['href'])

    base_url='https://q.stock.sohu.com'
    
    if len(report_links) == 0:
        print("未找到报告链接,请手动查询，或重新输入")
        return None
    else:
        url=base_url+report_links[0]
        print(url)
        return url


    # 股票报告链接



def get_report(lianjie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(lianjie, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 股票名称
    text = soup.find('pre').text
    #print(report)


    pattern = r"(联系人和联系方式)\r\s*\n*(.*?)(?=\n*\s*[一二三四五六七八九十]+、|$)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        # 提取匹配的标题和内容
        title = match.group(1)
        content = match.group(2).strip()
        print(f"找到标题：{title}")
        print("内容：")
        print(content)
        return content
    else:
        print("未找到指定的标题")
        return None
    
code='000892'
url=get_report_url(code)
get_report(url)