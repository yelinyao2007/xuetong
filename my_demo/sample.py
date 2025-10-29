#!/usr/bin/env python3
import argparse
import openvino_genai
from modelscope import snapshot_download
import os
import json
from datetime import datetime


class VideoTutorAssistant:
    def __init__(self, model_dir=None, device="CPU"):
        """初始化视频辅导助手"""
        print("🚀 初始化视频辅导助手...")

        # 自动下载或使用指定模型
        if model_dir and os.path.exists(model_dir):
            self.model_dir = model_dir
        else:
            print("📥 下载Qwen2.5-VL模型...")
            self.model_dir = snapshot_download("Qwen/Qwen2.5-VL-7B-Instruct-Int4")

        print(f"📁 使用模型路径: {self.model_dir}")

        # 初始化管道
        self.pipe = openvino_genai.LLMPipeline(self.model_dir, device)
        self.config = openvino_genai.GenerationConfig()
        self.config.max_new_tokens = 1024
        self.config.temperature = 0.7

        print("✅ 视频辅导助手初始化完成!")

    def streamer(self, subword):
        """流式输出回调函数"""
        print(subword, end='', flush=True)
        return openvino_genai.StreamingStatus.RUNNING

    def generate_video_script(self, topic, grade_level, duration="3分钟", style="动画"):
        """生成视频脚本"""
        prompt = f"""
        你是一个专业的视频制作助手，专门帮助学生通过视频理解学习内容。

        作业题目：{topic}
        学生年级：{grade_level}
        视频时长：{duration}
        视频风格：{style}

        请生成一个完整的视频制作方案，包括：

        【视频大纲】
        1. 核心概念解析
        2. 学习目标
        3. 视频结构

        【分镜脚本】
        按照时间顺序描述每个场景的内容、视觉元素和讲解要点

        【视觉设计】
        1. 主要视觉元素
        2. 颜色搭配建议
        3. 动画效果建议

        【音频建议】
        1. 背景音乐风格
        2. 音效建议
        3. 解说词风格

        【教育价值】
        1. 关键知识点
        2. 常见误区提醒
        3. 互动环节建议

        请用中文回答，内容要生动有趣，适合目标年龄段学生。
        """

        print(f"\n🎬 正在为「{topic}」生成{style}风格视频方案...\n")
        print("=" * 60)

        result = self.pipe.generate(prompt, self.config, self.streamer)
        print("\n" + "=" * 60)

        return result.texts[0]

    def analyze_homework(self, homework_text):
        """分析作业题目"""
        prompt = f"""
        分析以下作业题目，并提供视频制作建议：

        「{homework_text}」

        请分析：
        1. 题目涉及的核心知识点
        2. 学生的可能困难点
        3. 最适合的视频表现形式
        4. 建议的视频时长和风格

        用简洁明了的中文回答。
        """

        print(f"\n📚 正在分析作业题目...\n")
        print("=" * 50)

        result = self.pipe.generate(prompt, self.config, self.streamer)
        print("\n" + "=" * 50)

        return result.texts[0]

    def generate_prompts_for_ai_tools(self, topic, tool_type="stable_diffusion"):
        """为AI视频生成工具创建提示词"""
        prompt = f"""
        为AI视频生成工具创建详细的提示词：

        主题：{topic}
        工具类型：{tool_type}

        请提供：
        1. 主要场景描述（英文，适合AI理解）
        2. 风格关键词
        3. 颜色和光线要求
        4. 构图建议
        5. 负面提示词（不希望出现的内容）

        同时提供中文解释。
        """

        print(f"\n🎨 正在生成AI工具提示词...\n")
        print("=" * 50)

        result = self.pipe.generate(prompt, self.config, self.streamer)
        print("\n" + "=" * 50)

        return result.texts[0]


def main():
    parser = argparse.ArgumentParser(description="🎬 智能视频辅导助手")
    parser.add_argument('--model_dir', help='模型路径（可选）')
    parser.add_argument('--device', default='CPU', help='运行设备: CPU 或 GPU')

    args = parser.parse_args()

    # 初始化助手
    assistant = VideoTutorAssistant(args.model_dir, args.device)

    print("\n" + "🌟" * 20)
    print("🌟   智能视频辅导助手 v1.0   🌟")
    print("🌟" * 20)
    print("\n欢迎使用！我可以帮你：")
    print("1. 📚 分析作业题目")
    print("2. 🎬 生成视频脚本")
    print("3. 🎨 创建AI工具提示词")
    print("4. 💡 退出程序")

    while True:
        try:
            print("\n" + "-" * 40)
            choice = input("请选择功能 (1/2/3/4): ").strip()

            if choice == '1':
                # 分析作业题目
                homework = input("请输入作业题目: ").strip()
                if homework:
                    assistant.analyze_homework(homework)

            elif choice == '2':
                # 生成视频脚本
                topic = input("学习主题: ").strip()
                grade = input("学生年级 (如: 初中/高中/大学): ").strip() or "初中"
                duration = input("视频时长 (如: 3分钟): ").strip() or "3分钟"
                style = input("视频风格 (如: 动画/实拍/白板): ").strip() or "动画"

                if topic:
                    script = assistant.generate_video_script(topic, grade, duration, style)

                    # 询问是否保存
                    save = input("\n💾 是否保存脚本到文件? (y/n): ").strip().lower()
                    if save == 'y':
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"video_script_{timestamp}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(f"主题: {topic}\n")
                            f.write(f"年级: {grade}\n")
                            f.write(f"时长: {duration}\n")
                            f.write(f"风格: {style}\n")
                            f.write("-" * 50 + "\n")
                            f.write(script)
                        print(f"✅ 脚本已保存到: {filename}")

            elif choice == '3':
                # 生成AI工具提示词
                topic = input("请输入视频主题: ").strip()
                tool_type = input("AI工具类型 (如: stable_diffusion/midjourney): ").strip() or "stable_diffusion"

                if topic:
                    prompts = assistant.generate_prompts_for_ai_tools(topic, tool_type)

                    # 询问是否保存
                    save = input("\n💾 是否保存提示词到文件? (y/n): ").strip().lower()
                    if save == 'y':
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"ai_prompts_{timestamp}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(f"主题: {topic}\n")
                            f.write(f"工具: {tool_type}\n")
                            f.write("-" * 50 + "\n")
                            f.write(prompts)
                        print(f"✅ 提示词已保存到: {filename}")

            elif choice == '4':
                print("👋 感谢使用智能视频辅导助手，再见！")
                break

            else:
                print("❌ 请输入有效的选择 (1/2/3/4)")

        except KeyboardInterrupt:
            print("\n👋 程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()