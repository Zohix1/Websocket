import os
import subprocess
import threading

from app.utils.save_img import save_image

# TODO：传入动作描述(或者传入角色/图像，让大模型生成动作描述，返回需要是JSON格式的)和output_path，返回bvh文件地址

class SegmentationService:
    def process_segmentation_task(self, image_data, text_prompt, usr, callback):
        """
        处理图像分割任务，启动线程执行模型，并在任务完成后调用 callback 返回结果。
        """
        output_path = os.path.join('C:\\Users\\Administrator\\Desktop\\FlaskConnect\\save', usr, 'segment')
        os.makedirs(output_path, exist_ok=True)
        image_path = os.path.join(output_path, 'origin_photo.jpg')

        # 保存图像文件
        save_image(image_data, image_path)

        # 启动线程，执行图像分割模型
        thread = threading.Thread(target=self.run_segment_model, args=(image_path, output_path, text_prompt, callback))
        thread.start()

    def run_segment_model(self, image_path, output_path, text_prompt, callback):
        # 构建模型调用命令
        command = [
            "D:\\Anaconda\\envs\\gs\\python.exe", "grounded_sam_demo.py",
            "--config", "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py",
            "--grounded_checkpoint", "checkpoints\\groundingdino_swint_ogc.pth",
            "--sam_checkpoint", "checkpoints\\sam_vit_h_4b8939.pth",
            "--input_image", image_path,
            "--output_dir", output_path,
            "--box_threshold", "0.15",
            "--text_threshold", "0.15",
            "--text_prompt", text_prompt,
            "--device", "cuda"
        ]

        # 运行命令并处理输出
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            callback({'error': stderr})
        else:
            # output_data = self.parse_output(output_path)

            # 这里直接返回路径因为除了图像列表之外还应该存储位置信息到JSON文件中
            callback(output_path)

    # def parse_output(self, output_path):
    #     """
    #     解析模型输出，获取分割后的图像路径列表。
    #     """
    #     segmented_images = []
    #     for filename in os.listdir(output_path):
    #         if filename.endswith('.png'):
    #             segmented_images.append(os.path.join(output_path, filename))
    #     return segmented_images
