import time


class TextGenerationService:
    def stream_text_generation(self, prompt):
        """
        模拟调用流式文本生成 API，并逐步返回生成的文本块。
        这里使用模拟生成，可以用实际的 API 替代（例如 OpenAI 的流式 API）。
        """
        # 模拟逐步生成的文本块
        for i in range(5):
            yield f"Generated text segment {i} for prompt: {prompt}"
            time.sleep(1)  # 模拟生成延迟
