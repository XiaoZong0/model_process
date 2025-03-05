# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:45:31 2025
对文件夹内的图片按照数字重命名

@author: zongx
"""

import os
import shutil
import glob

root_dir = 'C:/Users/zongx/Desktop/results'

# 验证目录存在
if not os.path.exists(root_dir):
    raise FileNotFoundError(f"目录 {root_dir} 不存在")

# 遍历所有output_开头的子文件夹
for subfolder in glob.glob(os.path.join(root_dir, "output_*")):
    if os.path.isdir(subfolder):
        # 获取子文件夹中所有MP4文件
        mp4_files = glob.glob(os.path.join(subfolder, "*.mp4"))
        
        # 移动每个MP4文件
        for mp4_file in mp4_files:
            filename = os.path.basename(mp4_file)
            dest_path = os.path.join(root_dir, filename)
            
            # 处理文件名冲突（自动覆盖）
            if os.path.exists(dest_path):
                print(f"警告：{filename} 已存在，将覆盖")
                
            shutil.move(mp4_file, dest_path)
            print(f"已移动：{filename}")

print("所有MP4文件移动完成！")