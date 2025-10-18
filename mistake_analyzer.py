from PIL import Image


class MistakeAnalyzer:
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.analysis_history = []

    def analyze_text_problem(self, subject, problem_text):
        """分析文本题目"""
        prompt = f"""
        你是一个资深{subject}老师，请分析以下学生错题：

        题目：{problem_text}

        请按以下结构分析：
        ## 知识点解析
        - 涉及的核心概念
        - 相关公式/定理

        ## 解题步骤
        1. 第一步...
        2. 第二步...

        ## 错误原因
        - 概念理解错误
        - 计算失误
        - 审题不清

        ## 举一反三
        - 同类题型1
        - 同类题型2

        ## 学习建议
        - 重点复习内容
        - 练习建议
        """

        inputs = self.model_loader.text_tokenizer(prompt, return_tensors="pt")
        outputs = self.model_loader.text_model.generate(**inputs, max_length=1500)
        response = self.model_loader.text_tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 保存分析记录
        self.analysis_history.append({
            'subject': subject,
            'problem': problem_text,
            'analysis': response
        })

        return response

    def analyze_image_problem(self, image_path, subject):
        """分析图片题目"""
        image = Image.open(image_path)

        prompt = f"请分析这张{subject}题目图片，识别题目内容并提供详细的解题分析和知识点讲解。"

        inputs = self.model_loader.vision_processor(image, prompt, return_tensors="pt")
        outputs = self.model_loader.vision_model.generate(**inputs, max_length=1500)
        response = self.model_loader.vision_processor.decode(outputs[0], skip_special_tokens=True)

        return response