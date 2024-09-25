import os


class Config:
    # 服务器名称
    SERVER_NAME = 'api.drawing2game.top'

    # 设置图片保存目录
    BASE_DIR = '/Users/zohix/Code/Pycharm/Drawing2game/Websocket/app/statics'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # 其他可能的配置项
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    DEBUG = True

    # 更多的配置项可以根据需要继续添加
