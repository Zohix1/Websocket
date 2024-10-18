import os
import subprocess
import threading

from app.utils.to_url import generate_url
from app.utils.to_path import translate_url


# TODO：接收bvh路径和图片以及output_path、动作名称，通过callback返回gif_url及动作名称

class AnimateService:
    def process_animate_task(self, image_url, bvh_path, usr, callback):
        """
        处理图像分割任务，启动线程执行模型，并在任务完成后调用 callback 返回结果。
        """
        image_path = translate_url(image_url)

        output_path = os.path.join('C:\\Users\\Administrator\\Desktop\\FlaskConnect\\save', usr)  # gif输出路径

        # 启动线程，执行图像分割模型
        thread = threading.Thread(target=self.run_animate_model, args=(image_path, output_path, bvh_path, callback),
                                  kwargs={'default': True})
        thread.start()

    def run_animate_model(self, image_path, output_path, bvh_path, callback):

        process = subprocess.Popen(
            ['D:\\Anaconda\\envs\\ad\\python.exe', 'image_to_animation.py', image_path, output_path, bvh_path],
            cwd='C:\\Users\\Administrator\\Desktop\\AnimatedDrawings\\examples',
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            callback({'error': stderr})
        else:
            # 返回url
            # TODO:确定生成的gif地址
            generate_url()
            callback(output_path)
