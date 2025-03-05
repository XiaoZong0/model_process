import cv2
import os
import numpy as np
from pathlib import Path

def detect_face(image):
    """人脸检测函数"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def smart_crop(image_path, output_dir, target_size=512):
    """智能人脸居中裁剪"""
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图像 {image_path}")
        return

    # 人脸检测
    faces = detect_face(img)
    if len(faces) == 0:
        print(f"警告：未检测到人脸 {image_path}")
        return

    # 取最大人脸
    (x, y, w, h) = max(faces, key=lambda f: f[2]*f[3])

    # 计算人脸中心
    face_center = (x + w//2, y + h//2)

    # 确定裁剪区域
    height, width = img.shape[:2]
    crop_size = min(height, width, max(w, h)*2)  # 动态调整裁剪大小

    # 计算裁剪边界
    start_x = max(0, face_center[0] - crop_size//2)
    end_x = min(width, face_center[0] + crop_size//2)
    start_y = max(0, face_center[1] - crop_size//2)
    end_y = min(height, face_center[1] + crop_size//2)

    # 边界修正
    if end_x - start_x < crop_size:
        if start_x == 0:
            end_x = crop_size
        else:
            start_x = end_x - crop_size
    if end_y - start_y < crop_size:
        if start_y == 0:
            end_y = crop_size
        else:
            start_y = end_y - crop_size

    # 执行裁剪
    cropped = img[start_y:end_y, start_x:end_x]

    # 调整尺寸
    if target_size is not None:
        cropped = cv2.resize(cropped, (target_size, target_size), 
                           interpolation=cv2.INTER_AREA)

    # 保存结果
    output_path = Path(output_dir) / Path(image_path).name
    cv2.imwrite(str(output_path), cropped)
    print(f"处理完成：{output_path}")

def batch_process(input_dir, output_dir):
    """批量处理目录中的图片"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = [f for f in input_dir.glob('*') if f.suffix.lower() in supported_formats]

    for idx, img_path in enumerate(image_files, 1):
        print(f"正在处理 ({idx}/{len(image_files)}): {img_path.name}")
        try:
            smart_crop(str(img_path), str(output_dir))
        except Exception as e:
            print(f"处理失败 {img_path}: {str(e)}")

if __name__ == "__main__":
    # 配置参数
    INPUT_DIR = "images"  # 输入目录
    OUTPUT_DIR = "cropped_faces"  # 输出目录
    
    # 执行批量处理
    batch_process(INPUT_DIR, OUTPUT_DIR)
    print("\n处理完成！输出目录:", OUTPUT_DIR)