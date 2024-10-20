# imports
import time  # for measuring time duration of API calls
from textwrap import dedent

from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

generate_prompt = '''
    
'''


# 返回示例：ChatCompletionChunk(id='chatcmpl-9lMgfRSWPHcw51s6wxKT1YEO2CKpd', choice=[Choice(delta=ChoiceDelta(content='',
# function_call=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)],
# created=1721075653, model='gpt-july-test', object='chat.completion.chunk', system_fingerprint='fp_e9b8ed65d2',
# usage=None)


class TextGenerationService:
    def generate_conversation(self, charactor_prompt: str):
        # 通过角色Prompt生成会话，并返回对话id

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": dedent(generate_prompt) + charactor_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "和小朋友打个招呼吧"},
                ],
                 }
            ],
            temperature=0.2,
            max_completion_tokens=300
        )
        # 返回创建的对话id，和第一次初始化人物时的打招呼信息
        return response['id'], response['choices'][0]['message']['content']

    def stream_conversation(self, text: str, conversation_id: str):
        # 通过对话id流式返回对话结果
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": dedent(generate_prompt) + charactor_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "和小朋友打个招呼吧"},
                ],
                 }
            ],
            temperature=0.2,
            max_completion_tokens=300
        )
        # 返回创建的对话id，和第一次初始化人物时的打招呼信息
        return response['id'], response['choices'][0]['message']['content']
