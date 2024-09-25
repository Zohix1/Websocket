import os
import threading
import subprocess
from app.utils.to_url import save_image_from_base64


class SegmentationService:
    def process_segmentation_task(self, image_data, text_prompt, usr, callback):
        """
        处理图像分割任务，启动线程执行模型，并在任务完成后调用 callback 返回结果。
        """
        output_path = os.path.join('C:\\Users\\Administrator\\Desktop\\FlaskConnect\\save', usr, 'segment')
        os.makedirs(output_path, exist_ok=True)
        image_path = os.path.join(output_path, 'origin_photo.jpg')

        # 保存图像文件
        save_image_from_base64(image_data, image_path)

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
            output_data = self.parse_output(output_path)
            callback(output_data)

    def parse_output(self, output_path):
        """
        解析图像分割输出，生成 JSON 数据格式。
        """
        output_data = []
        for filename in os.listdir(output_path):
            if filename.endswith('.png'):
                full_file_path = os.path.join(output_path, filename)
                label = self.extract_label_from_filename(filename)
                img_url = generate_image_url(full_file_path)
                output_data.append({'file': img_url, 'label': label})
        return output_data

    def extract_label_from_filename(self, filename):
        """
        从文件名中提取标签。
        """
        return filename.split('.')[0]