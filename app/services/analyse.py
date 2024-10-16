import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from textwrap import dedent
from openai import OpenAI
from app.utils import generate_url
from app.models.Analyse_result import AnalyseResult
from app.models.image_info import ImageInfo

# TODO:填写apikey
client = OpenAI(api_key="your_api_key_here")

MODEL = "gpt-4o-mini"

# 图片分析提示词
analyse_prompt = '''
    我需要将孩子绘画中的各种元素置于作为游戏中的元素，并根据其特别的外形特征、所处的具体场景赋予这些绘画
    元素特殊的游戏内属性。
    同时对于原图中的指定物品或人物，需要按照以下约束为其指定个性化的属性或动作：
    - is_character: bool型变量，判断元素是否为人/或画出了四肢的角色，是则返回ture，反之返回false
    - Action: 当is_character为true时，根据元素特征及结合原图场景，用英文给出人物会在该场景下做的简单动作描述，
    如一个Action中：‘action：plow’‘description:A farmer is plowing the land.’。
    若is_character为false，则action_description列表为null。
    - personality_prompt: 当is_character为true时，根据人物特征及绘图场景为角色生成一段专属性格Prompt
    ，用于不同角色之间的对话，需要使用中文。若is_character为false，则personality_prompt为null。
    -Function：当is_character为false时，为物品元素赋予专属的互动展示属性，用英文给出物品的功能描述，
    Function与Action类似，若is_character为true则item_functions为null。
'''


# 获取图片的分析结果
def get_image_analysis(origin_image_url: str, image_url: str):
    # image_description = f"图片路径为 {image_path}"

    # 发送请求到OpenAI API进行分析
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": dedent(analyse_prompt)},
            {"role": "user", "content": [
                {"type": "text", "text": "第一张为原图片url，第二张为需要进行分析的对象图片url："},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": origin_image_url,
                        "detail": "low"
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": "low"
                    },
                }, ],
             }
        ],
        # max_tokens=300,
        response_format=AnalyseResult,
    )

    return completion.choices[0].message.parsed


# 图像分析服务类
class AnalyseService:
    def __init__(self, origin_image_url, folder_path):
        """
        初始化时读取文件夹中的所有图像及其位置 JSON 信息。
        """
        self.origin_image_url = origin_image_url
        self.folder_path = folder_path
        self.image_infos = []  # 保存所有图像信息的列表

        # 读初始化：取文件夹中的图像文件
        self._load_images_from_folder()

    def _load_images_from_folder(self):
        """
        从文件夹中读取图像及其位置信息，保存为 ImageInfo 对象。
        """
        # 找到 JSON 文件并读取
        json_file = None
        for file in os.listdir(self.folder_path):
            if file.endswith('.json'):
                json_file = os.path.join(self.folder_path, file)
                break

        position_data = {}
        # 获取物品位置信息
        # TODO：修改segment函数，使其存好图片和JSON文件
        if json_file:
            with open(json_file, 'r', encoding='utf-8') as f:
                position_data = json.load(f)

        # 遍历文件夹中的图像文件，并将其加入 image_infos 中
        for file in os.listdir(self.folder_path):
            if file.lower().endswith('.png'):
                image_path = os.path.join(self.folder_path, file)
                label = os.path.splitext(file)[0]  # 使用文件名作为初始标签
                position_info = position_data.get(file, {})  # 获取物品的位置信息
                image_info = ImageInfo(image_path, label, position_info)
                self.image_infos.append(image_info)

    def _process_single_image(self, image_info):
        """
        处理单张图片，生成其URL并使用OpenAI进行内容分析。
        """
        # 生成图片URL
        processed_image_url = generate_url(image_info.image_path)

        # 调用OpenAI分析图片内容
        analysis_result = get_image_analysis(self.origin_image_url, processed_image_url)

        # 返回结构化结果
        return {
            'file': processed_image_url,
            'analyse_result': analysis_result,
            'position': image_info.position_info,
            'status': 'processed'
        }

    def process_segmented_images(self, callback, max_workers=5):
        """
        使用多线程处理图像，并流式返回处理结果。

        Args:
            callback: 回调函数，用于流式返回处理结果
            max_workers: 最大线程数，控制并发量
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有图像的处理任务，并获取 future-to-image 映射
            future_to_image = {executor.submit(self._process_single_image, image_info): image_info for image_info in
                               self.image_infos}

            # 逐个处理已完成的任务，并调用 callback 进行流式返回
            for future in as_completed(future_to_image):
                try:
                    result = future.result()
                    callback(result)  # 调用回调函数返回处理结果
                except Exception as e:
                    # 发生异常时调用回调函数并返回错误
                    callback({'error': str(e)})
