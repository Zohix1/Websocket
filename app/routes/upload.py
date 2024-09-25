import uuid
from flask import Blueprint, request, jsonify
import os
from flask import current_app

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'code': 1, 'message': 'No file part', 'data': None}), 400
    file = request.files['file']
    # 检查是否选择了文件
    if file.filename == '':
        return jsonify({'code': 1, 'message': 'No selected file', 'data': None}), 400
    # 生成唯一的文件名
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    # 保存文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    # 保存文件
    file.save(file_path)
    # 生成文件的访问URL
    file_url = f"http://{request.host}/save/uploads/{filename}"
    # 返回带有code, message和data的JSON响应
    return jsonify({'code': 0, 'message': 'File uploaded successfully', 'data': file_url}), 200
