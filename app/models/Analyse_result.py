from pydantic import BaseModel


# 可以利用大模型制定角色的性格、移动路径

class AnalyseResult(BaseModel):

    # 是否为人物形象
    is_character: bool

    # 动作描述
    class Action(BaseModel):
        action: str
        description: str
    action_description: list[Action]

    # 人物性格提示
    personality_prompt: str

    class Function(BaseModel):
        function: str
        description: str

    # 物品功能
    item_functions: list[Function]

