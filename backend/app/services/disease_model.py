import base64
import os
from pathlib import Path
from openai import OpenAI

# 复用 llm_client 的配置，或者单独配置
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("TEA_LLM_API_KEY", "sk-proj-placeholder")
BASE_URL = os.getenv("TEA_LLM_BASE_URL", "https://api.openai.com/v1")
VISION_MODEL_NAME = os.getenv("TEA_LLM_VISION_MODEL", "qwen-vl-max") # Default for Ali

try:
    # 注意: Qwen VL 调用方式可能稍有不同，但如果是 OpenAI 兼容接口，通常只需换模型名
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
except Exception as e:
    print(f"Warning: OpenAI client init failed in disease_model: {e}")
    client = None

def encode_image(image_path: Path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class DiseaseModel:
    """
    使用视觉大模型进行病虫害诊断
    Using Vision LLM for disease detection
    """

    def predict(self, image_path: Path) -> dict:
        global client
        if not client:
             return {
                "disease_type": "Unknown (Service Unavailable)",
                "confidence": 0.0,
                "advice": "无法连接到智能诊断服务，请检查网络或 API 配置。",
            }

        try:
            # 编码图片
            base64_image = encode_image(image_path)
            
            # Debug info
            print(f"Calling Vision Model: {VISION_MODEL_NAME} at {BASE_URL}")

            response = client.chat.completions.create(
                model=VISION_MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个茶叶病虫害诊断专家。请分析这张茶叶图片。如果不包含茶叶，请说明。如果是病虫害，请指出名称、置信度（0-1）和防治建议。请以JSON格式返回，包含 keys: disease_type (string), confidence (float), advice (string)。如果无法识别，disease_type 为 'Unknown'。"
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "请诊断这张图片中的茶叶病害。"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300,
                response_format={ "type": "json_object" } # 强制 JSON 输出
            )
            
            import json
            result_text = response.choices[0].message.content
            # 简单的错误处理，防止 JSON 解析失败
            try:
                result_json = json.loads(result_text)
                return {
                    "disease_type": result_json.get("disease_type", "Unknown"),
                    "confidence": result_json.get("confidence", 0.0),
                    "advice": result_json.get("advice", "无建议"),
                }
            except json.JSONDecodeError:
                print(f"JSON Parse Error: {result_text}")
                return {
                    "disease_type": "Parse Error",
                    "confidence": 0.0,
                    "advice": f"模型返回格式错误: {result_text[:50]}...",
                }

        except Exception as e:
            print(f"Vision API Error: {e}")
            return {
                "disease_type": "API Error",
                "confidence": 0.0,
                "advice": f"诊断服务出错: {str(e)}",
            }

