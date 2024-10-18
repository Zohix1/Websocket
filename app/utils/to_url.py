import os
import base64

from flask import url_for, current_app


def generate_url(file_path):
    relative_path = os.path.relpath(file_path, current_app.static_folder)
    relative_path = relative_path.replace('\\', '/')  # 替换为 URL 友好的分隔符
    # 使用 Flask 的 url_for 生成静态文件的 URL
    # 假设你的静态文件都在 'static' 目录下，这个目录在你的 Flask app 配置中设置为 static_folder
    return url_for('static', filename=relative_path, _external=True)

