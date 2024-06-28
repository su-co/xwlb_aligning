import os
import json

# 文件路径
m4a_dir = '/media/as/ASNAS1/humiao/xwlb_m4a'
text_all_dir = '/media/as/ASNAS1/humiao/xwlbText/text_all'
json_file = '/media/as/ASNAS1/humiao/xwlbText/recording2book_all.json'

# 读取JSON文件
with open(json_file, 'r') as f:
    mapping = json.load(f)

# 获取JSON文件中记录的所有m4a文件和text文件的路径
m4a_files_in_json = set(mapping.keys())
text_files_in_json = set(os.path.join(text_all_dir, os.path.basename(path)) for path in mapping.values())

# 获取实际文件夹中的所有m4a文件和text文件
m4a_files_actual = set()
for root, _, files in os.walk(m4a_dir):
    for file in files:
        if file.endswith('.m4a'):
            m4a_files_actual.add(os.path.join(root, file))

text_files_actual = set()
for root, _, files in os.walk(text_all_dir):
    for file in files:
        text_files_actual.add(os.path.join(root, file))

# 找到实际文件夹中未在JSON文件中记录的m4a文件和text文件
m4a_files_to_delete = m4a_files_actual - m4a_files_in_json
text_files_to_delete = text_files_actual - text_files_in_json

# 删除未在JSON文件中记录的m4a文件
for file_path in m4a_files_to_delete:
    print(f"Deleting m4a file: {file_path}")
    os.remove(file_path)

# 删除未在JSON文件中记录的text文件
for file_path in text_files_to_delete:
    print(f"Deleting text file: {file_path}")
    os.remove(file_path)

print("Cleanup completed.")