import requests
from bs4 import BeautifulSoup
import time

# 读取txt文件中的链接
def read_links_from_file(file_path):
    links = []
    with open(file_path, 'r') as file:
        for line in file:
            links.append(line.strip())
    return links

# 请求链接并保存HTML内容
def save_html_from_links(links, save_location):
    for link in links:
        retries = 3  # 设置重试次数
        while retries > 0:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    html_content = response.text
                    # 解析HTML内容
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # 提取文件名
                    file_name = link.split('=')[-1] + '.html'
                    # 拼接保存路径
                    file_path = f"{save_location}/{file_name}"
                    # 保存HTML内容到文件
                    with open(file_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(html_content)
                    print(f'Saved {file_path}')
                    break  # 请求成功，退出重试循环
                else:
                    print(f'Failed to fetch {link}, status code: {response.status_code}')
                    retries -= 1
                    time.sleep(1)  # 休眠1秒后重试
            except requests.exceptions.ConnectionError as e:
                print(f'Connection error occurred: {e}')
                retries -= 1
                time.sleep(1)  # 休眠1秒后重试
        else:
            print(f'Failed to fetch {link} after retrying.')

if __name__ == "__main__":
    # 文件路径
    file_path = 'D:/yutu/dev/data/jpg/人脸识别/已知人脸信息照片/全网通缉/data/通缉令列表链接.txt'
    # 保存位置
    save_location = 'D:\yutu\dev\data\jpg\人脸识别\已知人脸信息照片\全网通缉\data\通缉令列表数据'
    # 读取链接
    links = read_links_from_file(file_path)
    # 请求链接并保存HTML内容
    save_html_from_links(links, save_location)
