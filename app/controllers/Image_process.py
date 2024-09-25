from app.services.segment import SegmentationService


class ImageProcess:
    def __init__(self):
        self.segmentation_service = SegmentationService()

    def handle_segmentation(self, image_data, text_prompt, usr, callback):
        """
        接受图像数据、文本提示和用户标识，处理图像分割任务。
        完成任务后调用 callback 返回结果给客户端。
        """
        self.segmentation_service.process_segmentation_task(image_data, text_prompt, usr, callback)
