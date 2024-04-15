import os

def print_directory_structure(structure, indent=0, file=None, root_name=None):
    """
    以目录树形式打印目录结构
    """
    if root_name is not None:
        print('    ' * indent + f'├── {root_name}', file=file)
        indent += 1
    for key, value in structure.items():
        if value is None:
            print('    ' * indent + f'└── {key}', file=file)
        else:
            print('    ' * indent + f'├── {key}', file=file)
            print_directory_structure(value, indent + 1, file=file)

def get_directory_structure(folder):
    """
    获取指定文件夹下所有文件的目录结构
    """
    structure = {}
    for root, dirs, files in os.walk(folder):
        current_dir = root.replace(folder, '').lstrip(os.sep)
        if current_dir:
            current_structure = structure
            for subdir in current_dir.split(os.sep):
                current_structure = current_structure.setdefault(subdir, {})
        else:
            current_structure = structure
        for file in files:
            current_structure[file] = None
    return structure

# 指定要获取目录结构的文件夹路径
folder_path = "D:/yutu/dev/data/jpg/人脸识别/已知人脸信息照片/全网通缉"

# 获取目录结构
directory_structure = get_directory_structure(folder_path)

# 指定要保存的文件名
output_file = "D:\yutu\dev\data\jpg\人脸识别\已知人脸信息照片\全网通缉\data\自述文件.txt"

# 打开文件并以 utf-8 编码写入
with open(output_file, 'w', encoding='utf-8') as f:
    # 以目录树形式打印目录结构到文件中
    print_directory_structure(directory_structure, file=f, root_name=os.path.basename(folder_path))

print(f"目录结构已保存到 {output_file}")
