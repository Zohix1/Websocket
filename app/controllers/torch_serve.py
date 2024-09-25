import threading
from app.services.torchserve_service import TorchServeService
from app.utils.torchserve_kill import kill


class TorchServeController:
    def __init__(self):
        self.torchserve_thread = None
        self.torchserve_service = TorchServeService()
        # 中断已启动的服务
        kill()

    def launch_torchserve(self):
        """启动 AnimatedDrawing 服务"""
        print("Starting TorchServe...")
        self.torchserve_thread = threading.Thread(target=self.torchserve_service.start_torchserve)
        self.torchserve_thread.start()
