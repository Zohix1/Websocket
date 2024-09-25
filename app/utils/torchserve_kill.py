# coding=utf-8
import socket
import time
import os
import psutil


def kill():
    """
    终止正在运行的 TorchServe 进程，如果存在
    """
    pid_file = 'C:\\Users\\Administrator\\AppData\\Local\\Temp\\.model_server.pid'

    # 检查 PID 文件是否存在
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as file:
            pid = int(file.read())
        try:
            # 尝试获取 PID 对应的进程
            process = psutil.Process(pid)
            # 检查进程是否还在运行，如果在运行则打印信息
            if process.is_running():
                print(f"Process {pid} is still running.")
        except psutil.NoSuchProcess:
            # 如果进程不存在，安全删除 PID 文件
            try:
                os.remove(pid_file)
                print(f"Removed orphan PID file for non-existing process {pid}.")
            except PermissionError as e:
                print(f"Cannot remove PID file: {e}. Check if the file is locked.")
    else:
        print("No PID file found, starting new instance.")
