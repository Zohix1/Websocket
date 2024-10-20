# TODO:接收文本Prompt、usr_id，流式返回文字的同时返回语音

from app.services.text_generate import TextGenerationService
from app.services.text_to_speech import TextToSpeechService
from flask_socketio import emit


class GenerateSpeakingController:
    def __init__(self):
        self.text_service = TextGenerationService()
        self.tts_service = TextToSpeechService()

    def handle_streaming_task(self, prompt, task_id):
        """
        协调文本生成和文字转语音的任务，并逐步返回结果。
        """
        # 逐步接收生成的文本，并同步进行文字转语音处理
        for text_chunk in self.text_service.stream_text_generation(prompt):
            # 通过 WebSocket 将生成的文本块发送给前端
            emit('text_generated', {'task_id': task_id, 'text_chunk': text_chunk})

            # 每次生成文本后，将其转换为语音并返回语音文件路径
            speech_file_path = self.tts_service.text_to_speech(text_chunk)
            emit('speech_generated', {'task_id': task_id, 'speech_file': speech_file_path})

        # 当所有文本生成完成后，发送任务完成消息
        emit('task_completed', {'task_id': task_id, 'status': 'completed'})