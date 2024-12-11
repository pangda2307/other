import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
#这里替换股票代码，然后用正则匹配获取链接，在进去年报，记得增加返回如果没有匹配到
#https://q.stock.sohu.com/cn/600839/cwbg.shtml
#此外，可以把股票代码和名字设置成匹配的，或者直接用Excel存储



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
        if "2023年年度报告" in link.text or "2023年度报告" in link.text or "2023年年度报告摘要" in link.text or "半年度报告" in link.text:
            if '英文' in link.text:
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
    print(f'年报获取状态：{response.status_code}')
    soup = BeautifulSoup(response.text, 'html.parser')

    # 股票名称
    text = soup.find('pre').text
    #print(report)


    pattern = r"(联系人和联系方式)\r\s*(.*?信箱.*?)(?=\s*[一二三四五六七八九十]+、|$)"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        pass
    else:
        pattern = r"(联系人和联系方式)(.*?信箱.*?)(?=\r)"
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
    
def contact(content):
    list_contact=content.split('\n')
    for i in list_contact:
        #-----------------------姓名-----------
        if '姓名' in i:
            name=i.split(' ')
            name = [x for x in name if x or x == 0]
            if name[-1].endswith('\r'):
                name[-1] = name[-1].rstrip('\r')
                
        #-----------------------电话-----------
        if '电话' in i:
            phone=i.split(' ')
            phone = [x for x in phone if x or x == 0]
            if phone[-1].endswith('\r'):
                phone[-1] = phone[-1].rstrip('\r')
        #-----------------------邮箱-----------
        if '信箱' in i or '邮箱' in i:
            email=i.split(' ')
            email = [x for x in email if x or x == 0]
            if email[-1].endswith('\r'):
                email[-1] = email[-1].rstrip('\r')
    
    return name,phone,email              


def get_stock():
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, '股票代码.xlsx')
    stock_excel=pd.read_excel(file_path,header=None,index_col=None)
    stock_code=stock_excel.iloc[:,0]
    stock_name=stock_excel.iloc[:,1]
    
    # 确保股票代码为6位数，不足6位的前面补0
    stock_code = stock_code.apply(lambda x: str(x).zfill(6))
    return stock_code,stock_name

def write_to_excel(stock_code, stock_name, name, phone, email, sheet):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, '上市公司信息.xlsx')
    
    df = pd.DataFrame({
        '股票代码': [stock_code],
        '股票名称': [stock_name],
        '姓名': [name],
        '电话': [phone],
        '邮箱': [email]
    })
    


    
    # 检查文件是否存在，如果不存在则创建文件
    if not os.path.exists(file_path):
        df.to_excel(file_path, sheet_name=sheet, index=False)
        return
    
    # 使用ExcelWriter以追加模式打开文件
    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl',if_sheet_exists='overlay') as writer:
        # 加载工作簿和工作表
        workbook = writer.book
        
        if sheet not in workbook.sheetnames:
                # 如果指定的工作表不存在，创建一个新的工作表并写入DataFrame，包括表头
                workbook.create_sheet(sheet)
                df.to_excel(writer, sheet_name=sheet, index=False)
        else:
            # 如果工作表已存在，获取工作表的最大行数
            worksheet = workbook[sheet]
            startrow = worksheet.max_row
            # 将DataFrame写入Excel文件，不写入表头
            df.to_excel(writer, sheet_name=sheet, index=False, startrow=startrow, header=False)

    
    
"""code=input("请输入股票代码：") 
lianjie=get_report_url(code)
print(lianjie)
content=get_report(lianjie)
contact(content)"""
sotck_code,stock_name=get_stock()
for i in range(len(sotck_code)):
    content=None#清空内容，避免重复
    #董秘信息写入
    try:
        lianjie=get_report_url(sotck_code[i])
        content=get_report(lianjie)
    except Exception as e:
        print(e)
    finally:
        try:
            if content:
                name,phone,email=contact(content)
                write_to_excel(sotck_code[i],stock_name[i],name[1],phone[1],email[1],'董秘')
            else:
                write_to_excel(sotck_code[i],stock_name[i],'','','','董秘')
        except:
            write_to_excel(sotck_code[i],stock_name[i],'','','','董秘')
        finally:
            #证券事务代表写入
            try:
                print(f"第{i+1}个股票")
                if content:
                    name,phone,email=contact(content)
                    write_to_excel(sotck_code[i],stock_name[i],name[2],phone[2],email[2],'证券事务代表')
                else:
                    write_to_excel(sotck_code[i],stock_name[i],'','','','证券事务代表')
            except:
                    write_to_excel(sotck_code[i],stock_name[i],'','','','证券事务代表')
    
    
        
    time.sleep(3)

print("完成")