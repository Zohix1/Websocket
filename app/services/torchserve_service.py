import os
import subprocess


class TorchServeService:
    base_path = "D:\\Anaconda\\envs"  # 设置 conda 基本路径

    def start_torchserve(self):
        """启动 TorchServe 服务"""

        # 更新环境变量
        env = os.environ.copy()
        env_path = os.path.join(self.base_path, "ad")
        env["PATH"] = os.path.join(env_path, "bin") + os.pathsep + env["PATH"]
        env['CUDA_VISIBLE_DEVICES'] = '0'

        # 启动 TorchServe 的命令
        command = [
            'D:\\Anaconda\\envs\\ad\\Scripts\\torchserve.exe',
            '--start',
            '--ts-config', '.\\torchserve\\config.properties',
            '--model-store', '.\\torchserve\\model-store',
            '--foreground'
        ]

        # 在后台启动 torchserve
        subprocess.Popen(command, cwd='C:\\Users\\Administrator\\Desktop\\AnimatedDrawings', env=env)
