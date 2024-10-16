from app import socketio
from app.controllers.Image_process import ImageProcess
from app.controllers.Generate_speak import TextController

# 实例化控制器
segmentation_controller = ImageProcess()
text_controller = TextController()


@socketio.on('segment_paintings')
def handle_segment_paintings(data):
    """
    接收来自客户端的 WebSocket 消息，处理图像分割与识别任务。
    """
    # TODO：发送请求时可以改为先upload，再发送url即可。改为无关键词识别后，不用发送分割Prompt/在文本提示里写上预先设定好的类别列表
    image_url = data['url']  # Base64 编码的图片
    text_prompt = data['prompt']  # 文本提示
    usr = data['usr']  # 用户身份标识

    # 调用控制器处理图像分割任务
    segmentation_controller.handle_segmentation(image_url, text_prompt, usr)


@socketio.on('start_streaming_task')
def handle_start_streaming_task(data):
    """
    WebSocket 事件：处理前端发起的流式生成请求，并逐步返回数据。
    """
    task_id = data.get('task_id')
    prompt = data.get('prompt')

    # if not prompt:
    #     emit('task_error', {'task_id': task_id, 'error': 'Missing prompt'})
    #     return

    # 启动流式文本生成和语音合成任务
    text_controller.handle_streaming_task(prompt, task_id)
