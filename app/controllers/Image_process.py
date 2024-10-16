from flask_socketio import emit

from app.services.segment import SegmentationService
from app.services.analyse import AnalyseService


class ImageProcess:
    def __init__(self, segmentation_service):
        self.segmentation_service = segmentation_service

    def handle_segmentation(self, image_data, text_prompt, usr):
        """
        处理图像分割，并在图像分割后进行进一步分析。
        """
        def image_processed_callback(result):
            emit('image_processed', {'usr': usr, 'result': result})

        def segmentation_completed_callback(output_path):
            # 分割任务完成后，初始化 AnalyseService
            self.analyse_service = AnalyseService(image_data, output_path)
            # 使用多线程分析处理分割图像
            self.analyse_service.process_segmented_images(image_processed_callback)

        self.segmentation_service.process_segmentation_task(image_data, text_prompt, usr, segmentation_completed_callback)
