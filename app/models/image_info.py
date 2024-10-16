# 定义一个类保存图像信息
class ImageInfo:
    def __init__(self, image_url, label, position_info=None):
        self.image_url = image_url  # 图像文件路径
        # self.label = label  # 图像标签（通过文件名获取）
        self.position_info = position_info  # 图像分割位置（来自 JSON 文件）
