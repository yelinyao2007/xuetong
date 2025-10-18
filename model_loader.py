# model_loader.py
import openvino as ov
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from PIL import Image
import numpy as np


class OpenVINOModelLoader:
    def __init__(self):
        self.core = ov.Core()
        self.compiled_model = None
        self.tokenizer = None

    def load_model_openvino_native(self):
        """使用OpenVINO原生方式加载模型"""
        try:
            model_id = "Qwen/Qwen2.5-0.5B-Instruct"

            # 1. 先加载原始模型和tokenizer
            print("📥 加载原始模型...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                trust_remote_code=True
            )

            # 2. 转换为ONNX，然后转为OpenVINO IR格式
            print("🔄 转换模型格式...")
            ov_model_path = self.convert_to_openvino(model_id)

            # 3. 加载OpenVINO模型
            print("⚡ 编译OpenVINO模型...")
            self.compiled_model = self.core.compile_model(ov_model_path, "CPU")

            print("✅ OpenVINO模型加载完成！")
            return True

        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False

    def convert_to_openvino(self, model_id):
        """将模型转换为OpenVINO格式"""
        import os
        ov_model_dir = "./openvino_model"

        if not os.path.exists(ov_model_dir):
            os.makedirs(ov_model_dir)

            # 使用OpenVINO的转换工具
            from openvino.tools import mo
            from openvino.runtime import serialize

            # 加载原始模型
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True,
                torch_dtype=torch.float32
            )

            # 创建示例输入
            dummy_input = self.tokenizer("Hello", return_tensors="pt")

            # 导出为ONNX
            torch.onnx.export(
                model,
                tuple(dummy_input.values()),
                f"{ov_model_dir}/model.onnx",
                input_names=list(dummy_input.keys()),
                output_names=["logits"],
                dynamic_axes={
                    key: {0: "batch_size", 1: "sequence_length"}
                    for key in dummy_input.keys()
                },
                opset_version=14
            )

            # 转换为OpenVINO IR
            ov_model = mo.convert_model(f"{ov_model_dir}/model.onnx")
            serialize(ov_model, f"{ov_model_dir}/openvino_model.xml")

        return ov_model_dir

    def generate(self, prompt, max_length=500):
        """使用OpenVINO模型生成文本"""
        if self.compiled_model is None:
            return "模型未加载"

        # 编码输入
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"]

        # 推理循环
        for _ in range(max_length):
            # 准备输入数据
            inputs_dict = {
                "input_ids": input_ids.numpy()
            }

            # OpenVINO推理
            results = self.compiled_model(inputs_dict)
            logits = results[0]

            # 获取下一个token
            next_token_logits = logits[0, -1, :]
            next_token = np.argmax(next_token_logits, axis=-1)

            # 添加到序列
            input_ids = torch.cat([
                input_ids,
                torch.tensor([[next_token]], dtype=torch.long)
            ], dim=-1)

            # 如果生成了结束符，停止生成
            if next_token == self.tokenizer.eos_token_id:
                break

        # 解码输出
        response = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
        return response