import time
from bs4 import BeautifulSoup
import os

# 指定文件夹路径
folder_path = r'D:\yutu\dev\data\jpg\人脸识别\已知人脸信息照片\全网通缉\data\通缉令列表数据'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取HTML内容
                html_content = file.read()
                # 使用Beautiful Soup解析HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                # 找到所有类属性为"screen_criminal_list"的div元素
                criminal_divs = soup.find_all('div', class_='screen_criminal_list')
                # 创建一个新的Beautiful Soup对象，用于存储提取出的div元素
                new_soup = BeautifulSoup('', 'html.parser')
                # 将找到的所有div元素添加到新的Beautiful Soup对象中
                for div in criminal_divs:
                    # 如果div元素没有子元素，则删除对应文件
                    if not div.findChildren():
                        os.remove(file_path)
                        break
                    new_soup.append(div)
            # 如果新的Beautiful Soup对象不为空，则将新的HTML内容写回原始文件
            if new_soup.contents:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(new_soup))
        except PermissionError:
            print(f"无法删除文件: {file_path}，可能因为其它程序正在使用。")
            continue
        except Exception as e:
            print(f"处理文件 {file_path} 时发生错误: {str(e)}")
            continue
        time.sleep(0.001)  # 延迟一秒钟
