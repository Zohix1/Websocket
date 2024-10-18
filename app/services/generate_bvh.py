import os
import subprocess
import threading

from app.utils.save_img import save_image


# TODO：传入动作描述(或者传入角色/图像，让大模型生成动作描述，返回需要是JSON格式的)和output_path，返回bvh文件地址

class GenerateBvhService:
    def process_generate_bvh_task(self, text_prompt, usr, callback):
        """
            通过文字生成bvh文件
        """
        output_path = os.path.join('C:\\Users\\Administrator\\Desktop\\FlaskConnect\\save', usr)  # gif输出路径
        os.makedirs(output_path, exist_ok=True)

        command = [
            "D:\\Anaconda\\envs\\mmc\\python.exe", "gen_t2m.py",
            "--gpu_id", "0",
            "--ext", "exp1",
            "--text_prompt", text_prompt,
            "--output_path", output_path
        ]
        # 运行脚本
        process = subprocess.Popen(command, cwd='C:\\Users\\Administrator\\Desktop\\momask-codes',
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            callback({'error': stderr})
        else:
            # TODO：修改outputpath为生成的bvh路径

            callback(output_path)
