from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer, AutoProcessor
import openvino as ov

MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'

class ModelLoader:
    def __init__(self):
        self.text_model = None
        self.vision_model = None
        self.text_tokenizer = None
        self.vision_processor = None

    def load_text_model(self):
        """加载Qwen3文本模型"""
        model_id = MODEL_ID

        # 使用OpenVINO优化版本
        self.text_model = OVModelForCausalLM.from_pretrained(
            model_id,
            export=True,
            device="CPU",  # 或 "GPU", "NPU"
            trust_remote_code=True
        )
        self.text_tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("✅ 文本模型加载完成")

    def load_vision_model(self):
        """加载Qwen3-VL多模态模型（用于图片题目分析）"""
        model_id = MODEL_ID

        self.vision_model = OVModelForCausalLM.from_pretrained(
            model_id,
            export=True,
            device="CPU",
            trust_remote_code=True
        )
        self.vision_processor = AutoProcessor.from_pretrained(model_id)
        print("✅ 视觉模型加载完成")