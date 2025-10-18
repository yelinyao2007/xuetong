# modelscope_loader.py
import os

# 强制使用ModelScope国内源
os.environ['USE_MODELSCOPE'] = 'True'

from modelscope import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM


class ModelScopeLoader:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_from_modelscope(self):
        """从魔塔ModelScope下载模型"""
        try:
            model_id = "qwen/Qwen2.5-0.5B-Instruct"

            print("📥 从ModelScope下载模型...")
            # 下载模型到本地缓存
            model_dir = snapshot_download(model_id)

            # 从本地加载
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_dir,
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                trust_remote_code=True,
                torch_dtype="auto",
                device_map="auto"
            )

            print("✅ ModelScope模型加载成功！")
            return True

        except Exception as e:
            print(f"❌ ModelScope加载失败: {e}")
            return False