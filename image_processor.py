from PIL import Image
import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.knowledge_points = {
            "数学": ["代数", "几何", "函数", "概率统计", "三角函数"],
            "物理": ["力学", "电学", "光学", "热学", "原子物理"],
            "化学": ["化学反应", "物质结构", "化学计算", "实验操作"],
            "语文": ["文言文", "现代文阅读", "作文", "古诗词"],
            "英语": ["语法", "阅读理解", "写作", "词汇"]
        }

    def preprocess_image(self, image_path):
        """预处理上传的图片"""
        image = Image.open(image_path)
        # 图像增强：提高文字识别率
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    def analyze_math_problem(self, image, model, processor):
        """分析数学题目"""
        prompt = """请分析这张数学题目图片，按以下格式回答：
        1. 题目内容：[提取的题目文本]
        2. 涉及知识点：[主要知识点]
        3. 解题思路：[步骤解析]
        4. 易错点：[常见错误]
        5. 同类题推荐：[2-3个类似题目]"""

        inputs = processor(image, prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=1000)
        response = processor.decode(outputs[0], skip_special_tokens=True)
        return response