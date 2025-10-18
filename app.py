import gradio as gr
from model_loader_v2 import ModelLoader
from mistake_analyzer import MistakeAnalyzer


class MistakeAnalysisApp:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.analyzer = None

    def initialize_models(self):
        """初始化模型"""
        self.model_loader.load_text_model()
        # 如果需要图片分析，取消下面注释
        # self.model_loader.load_vision_model()
        self.analyzer = MistakeAnalyzer(self.model_loader)
        return "✅ 模型初始化完成！"

    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(title="中学生错题分析助手") as demo:
            gr.Markdown("# 🎯 中学生错题智能分析助手")
            gr.Markdown("上传你的错题，获取专业的知识点分析和学习建议")

            with gr.Row():
                with gr.Column():
                    subject = gr.Dropdown(
                        choices=["数学", "物理", "化学", "语文", "英语"],
                        label="选择学科",
                        value="数学"
                    )

                    problem_type = gr.Radio(
                        choices=["文字题目", "图片题目"],
                        label="题目类型",
                        value="文字题目"
                    )

                    problem_text = gr.Textbox(
                        lines=4,
                        label="输入题目内容",
                        placeholder="在这里粘贴或输入题目内容..."
                    )

                    image_input = gr.Image(
                        label="上传题目图片",
                        type="filepath",
                        visible=False
                    )

                    analyze_btn = gr.Button("开始分析", variant="primary")

                with gr.Column():
                    output = gr.Markdown(label="分析结果")

            # 根据题目类型显示/隐藏输入框
            problem_type.change(
                lambda x: (gr.update(visible=x == "文字题目"), gr.update(visible=x == "图片题目")),
                inputs=[problem_type],
                outputs=[problem_text, image_input]
            )

            analyze_btn.click(
                self.analyze_problem,
                inputs=[subject, problem_type, problem_text, image_input],
                outputs=[output]
            )

        return demo

    def analyze_problem(self, subject, problem_type, problem_text, image_path):
        """分析问题的主函数"""
        if problem_type == "文字题目" and not problem_text.strip():
            return "❌ 请输入题目内容"
        elif problem_type == "图片题目" and image_path is None:
            return "❌ 请上传题目图片"

        try:
            if problem_type == "文字题目":
                analysis = self.analyzer.analyze_text_problem(subject, problem_text)
            else:
                analysis = self.analyzer.analyze_image_problem(image_path, subject)

            return f"## 📚 分析结果\n\n{analysis}"

        except Exception as e:
            return f"❌ 分析过程中出现错误：{str(e)}"


if __name__ == "__main__":
    app = MistakeAnalysisApp()

    # 初始化模型
    print("正在加载模型...")
    app.initialize_models()

    # 启动界面
    demo = app.create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)