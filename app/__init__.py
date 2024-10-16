from flask import Flask
from flask_socketio import SocketIO

from app.controllers.torch_serve import TorchServeController
from app.routes.upload import upload_bp
from config import Config

socketio = SocketIO()


def create_app():
    # 修改静态目录路径
    app = Flask(__name__, static_folder='C:\\Users\\Administrator\\Desktop\\FlaskConnect\\save')
    app.config.from_object(Config)

    # 注册蓝图
    # from app.routes.main import main_bp
    # app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp, url_prefix='/api')  # 给所有上传接口加上 /api 前缀

    # 初始化 SocketIO
    socketio.init_app(app)

    # 实例化控制器
    torchserve_controller = TorchServeController()

    # 使用应用上下文立即启动 TorchServe
    with app.app_context():
        torchserve_controller.launch_torchserve()

    # 导入 WebSocket 事件
    from app import events

    return app
