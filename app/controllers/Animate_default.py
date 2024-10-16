from flask_socketio import emit

from app.services.segment import SegmentationService
from app.services.analyse import AnalyseService


# TODO:走路动画统一使用预制bvh，待机动画通过momask进行生成，可以生成多个动作

class ImageProcess:
    def __init__(self):
        self.segmentation_service = SegmentationService()
        self.analyse_service = AnalyseService()

    def handle_segmentation(self, image_data, text_prompt, usr):
        """
        接受图像数据、文本提示和用户标识，处理图像分割任务。
        在任务完成后启动进一步的逐个图像处理，并通过 WebSocket 逐个返回结果。
        """

        # 定义逐个处理后的结果回调函数
        def image_processed_callback(result):
            emit('image_processed', {'usr': usr, 'result': result})

        # 图像分割任务完成后的回调，接收分割后的图像列表，并逐个处理
        def segmentation_completed_callback(output_path):
            # 对逐个图像进行进一步处理
            self.analyse_service.process_segmented_images(output_path, image_processed_callback)

        # 调用图像分割任务
        self.segmentation_service.process_segmentation_task(image_data, text_prompt, usr,
                                                            segmentation_completed_callback)
