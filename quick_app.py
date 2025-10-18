# quick_app.py
import gradio as gr
from model_loader import OpenVINOModelLoader
import time


class QuickContestApp:
    def __init__(self):
        self.model_loader = OpenVINOModelLoader()

    def initialize(self):
        """快速初始化"""
        print("🚀 快速启动OpenVINO应用...")
        start_time = time.time()

        success = self.model_loader.load_model_openvino_native()

        if success:
            load_time = time.time() - start_time
            return f"✅ 初始化完成！耗时: {load_time:.2f}秒"
        else:
            return "❌ 初始化失败，使用备用方案..."

    def create_demo(self):
        """创建演示界面"""
        with gr.Blocks(theme=gr.themes.Soft(), title="英特尔AI PC错题分析") as demo:
            gr.Markdown("""
            # 🏆 英特尔AI PC - 错题分析助手
            ### 基于OpenVINO + Qwen模型的本地AI应用
            """)

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📝 输入错题")
                    subject = gr.Dropdown(
                        ["数学", "物理", "化学", "英语", "语文"],
                        value="数学", label="学科"
                    )
                    question = gr.Textbox(
                        lines=3,
                        label="题目内容",
                        placeholder="例如: 解方程: x² - 5x + 6 = 0"
                    )
                    btn = gr.Button("🚀 分析错题", variant="primary")

                with gr.Column():
                    gr.Markdown("### 📊 分析结果")
                    output = gr.Markdown("等待分析...")

            # 示例题目
            examples = gr.Examples(
                examples=[
                    ["数学", "已知三角形ABC，AB=3, AC=4, BC=5，求角A的度数"],
                    ["物理", "一个物体从80米高处自由落下，求落地时的速度"],
                    ["化学", "写出盐酸和氢氧化钠反应的化学方程式"]
                ],
                inputs=[subject, question]
            )

            btn.click(
                self.analyze_question,
                inputs=[subject, question],
                outputs=output
            )

        return demo

    def analyze_question(self, subject, question):
        """分析问题"""
        if not question.strip():
            return "❌ 请输入题目内容"

        prompt = f"""
        你是一个专业的{subject}老师，请分析以下学生错题：

        题目：{question}

        请按以下格式回答：
        ## 知识点分析
        - 涉及的核心概念
        - 相关公式/定理

        ## 解题步骤  
        1. 第一步...
        2. 第二步...

        ## 常见错误
        - 错误类型1...
        - 错误类型2...

        ## 学习建议
        - 重点复习...
        - 练习建议...
        """

        try:
            response = self.model_loader.generate(prompt, max_length=800)
            return f"## 📚 分析结果\n\n{response}"
        except Exception as e:
            return f"❌ 分析失败: {str(e)}"


# 立即运行
if __name__ == "__main__":
    app = QuickContestApp()

    print("=" * 50)
    print("🏆 英特尔AI PC比赛 - 快速启动版")
    print("=" * 50)

    status = app.initialize()
    print(status)

    if "完成" in status:
        demo = app.create_demo()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            show_error=True
        )