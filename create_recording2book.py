import os
import json

# 文件夹路径
xwlbText_folder = '/media/as/ASNAS1/humiao/xwlbText/text_all'
xwlb_m4a_folder = '/media/as/ASNAS1/humiao/xwlb_m4a/all'

# 获取xwlbText文件夹中的文件名（日期）
text_files = {f for f in os.listdir(xwlbText_folder) if os.path.isfile(os.path.join(xwlbText_folder, f))}

# 获取xwlb_m4a文件夹中的文件名（日期+m4a后缀），并去掉后缀
m4a_files = {f[:-4] for f in os.listdir(xwlb_m4a_folder) if os.path.isfile(os.path.join(xwlb_m4a_folder, f)) and f.endswith('.m4a')}

# 找到两个文件夹中都存在的日期
common_dates = text_files & m4a_files

# 构建输出格式的字典
output_dict = {}
for date in common_dates:
    m4a_path = os.path.join(xwlb_m4a_folder, f"{date}.m4a")
    text_path = os.path.join(xwlbText_folder, date.split('_')[0])
    output_dict[m4a_path] = text_path

# 写入JSON文件
with open('/media/as/ASNAS1/humiao/xwlbText/recording2book_all.json', 'w') as json_file:
    json.dump(output_dict, json_file, indent=4)