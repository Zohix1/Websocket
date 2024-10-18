from flask_socketio import emit

from app.services.animate import AnimateService

from app.services.generate_bvh import GenerateBvhService


# TODO:走路动画统一使用预制bvh，待机动画通过momask进行生成，可以生成多个动作

class AnimatedProcess:
    def __init__(self, animate_service):
        self.animate_service = animate_service

        self.generate_bvh_service = GenerateBvhService()

    def handle_segmentation(self, image_url, action_prompt_1, action_prompt_2, usr):
        """
        按照顺序生成默认动作、待机动作和个性化动作
        """
        def animate_default_callback(result):
            emit('image_processed', {'usr': usr, 'result': result})

        def animate_usingtext_callback(bvh_path):
            self.animate_service.process_animate_task(image_url, bvh_path, usr, animate_default_callback)

        # 生成跑动动作
        run_bvh_path = 'C:\\Users\\Administrator\\Desktop\\AnimatedDrawings\\examples\\bvh\\rokoko\\running.bvh'

        self.animate_service.process_animate_task(image_url, run_bvh_path, usr, animate_default_callback)

        # 生成动作1（待机）
        self.generate_bvh_service.process_generate_bvh_task(action_prompt_1, usr, animate_usingtext_callback)

        # 生成动作2（自定义动作）
        self.generate_bvh_service.process_generate_bvh_task(action_prompt_1, usr, animate_usingtext_callback)
