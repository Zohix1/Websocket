import time
import os
# from gtts import gTTS  # 使用 gTTS 作为示例


class TextToSpeechService:
    def text_to_speech(self, text, output_folder='app/static/files'):
        """
        将文本转为语音，并保存为 mp3 文件。
        """
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'{text[:10]}.mp3')  # 取文本前10个字符作为文件名
        # tts = gTTS(text)
        # tts.save(output_file)

        time.sleep(1)  # 模拟生成延迟
        return output_file  # 返回生成的文件路径