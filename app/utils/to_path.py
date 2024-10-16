import os
import base64
from urllib.parse import urlparse

from flask import url_for, current_app


def translate_url(image_url):
    parsed_url = urlparse(image_url)
    url_path = parsed_url.path
    # 假设 URL 路径中包含了 static_folder 之后的部分，需要移除前导的 '/save'
    relative_path = url_path.lstrip('/save')
    # 构建绝对路径
    image_path = os.path.join(current_app.static_folder, relative_path.replace('/', '\\'))

    # 返回文件路径
    return image_path
