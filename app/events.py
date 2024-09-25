from app import socketio
from flask_socketio import emit
from app.controllers.Image_process import ImageProcess

segmentation_controller = ImageProcess()


@socketio.on('segment_paintings')
def handle_segment_paintings(data):
    """
    接收来自客户端的 WebSocket 消息，处理图像分割与识别任务。
    """
    image_data = data['image']  # Base64 编码的图片
    text_prompt = data['prompt']  # 文本提示
    usr = data['usr']  # 用户身份标识

    # 调用控制器处理图像分割任务
    segmentation_controller.handle_segmentation(image_data, text_prompt, usr, emit_task_result)


def emit_task_result(output_data):
    """
    任务完成后，将分割结果通过 WebSocket 发送给客户端。
    """
    emit('segment_completed', {'images': output_data})
