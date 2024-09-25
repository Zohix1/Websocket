import os
import base64

def save_image_from_base64(image_data, file_path):
    """
    将 Base64 编码的图像数据保存为文件。
    """
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(image_data))

def generate_image_url(file_path):
    """
    根据文件路径生成可访问的 URL。
    """
    return f'/static/uploads/{os.path.basename(file_path)}'