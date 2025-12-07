import os
from pathlib import Path
from sqlalchemy.orm import Session
from openai import OpenAI
from ..schemas import ChatRequest
from ..models import TeaGarden, Plot, SensorRecord, SensorRule

# 获取API Key和Base URL (默认使用OpenAI格式)
# 建议在环境变量中配置 TEA_LLM_API_KEY 和 TEA_LLM_BASE_URL
# 获取API Key和Base URL (默认使用OpenAI格式)
# 建议在环境变量中配置 TEA_LLM_API_KEY 和 TEA_LLM_BASE_URL
from dotenv import load_dotenv
load_dotenv() # Force load to be safe if imported independently

API_KEY = os.getenv("TEA_LLM_API_KEY", "sk-proj-...")
BASE_URL = os.getenv("TEA_LLM_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("TEA_LLM_MODEL", "qwen-turbo") # Default to qwen-turbo since user mentioned Ali

print(f"DEBUG: LLM Client Init. Key starts with: {API_KEY[:4]}..., BaseURL: {BASE_URL}, Model: {MODEL_NAME}")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def get_knowledge_base_content() -> str:
    """读取 backend/knowledge_base 目录下的所有 md 文件内容"""
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        return ""
    
    content = []
    for f in kb_path.glob("*.md"):
        try:
            # 尝试 UTF-8
            text = f.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Fallback to GBK (Common on Windows)
                text = f.read_text(encoding='gbk')
            except Exception as e:
                print(f"Error reading {f} with GBK: {e}")
                continue
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue
            
        content.append(f"--- {f.name} ---\n{text}")
    return "\n\n".join(content)

from datetime import datetime, timedelta
from sqlalchemy import func

def get_recent_sensor_stats(plot_id: int, db: Session) -> str:
    """
    获取最近7天的传感器数据统计 (天气 + 土壤)
    Get sensor statistics for the last 7 days
    """
    if not plot_id:
        return ""

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # 查询最近7天的数据
    records = db.query(SensorRecord).filter(
        SensorRecord.plot_id == plot_id,
        SensorRecord.timestamp >= seven_days_ago
    ).all()
    
    if not records:
        return "最近7天无传感器数据记录。"

    # 简单统计
    temps = [r.temperature for r in records if r.temperature is not None]
    humids = [r.humidity for r in records if r.humidity is not None]
    soils = [r.soil_moisture for r in records if r.soil_moisture is not None]
    
    stats_text = ["【最近7天环境数据统计】"]
    
    if temps:
        stats_text.append(f"- 空气温度: 平均 {sum(temps)/len(temps):.1f}°C, 最高 {max(temps):.1f}°C, 最低 {min(temps):.1f}°C")
    
    if humids:
        stats_text.append(f"- 空气湿度: 平均 {sum(humids)/len(humids):.1f}%, 最高 {max(humids):.1f}%, 最低 {min(humids):.1f}%")
        
    if soils:
        stats_text.append(f"- 土壤湿度: 平均 {sum(soils)/len(soils):.1f}%, 最高 {max(soils):.1f}%, 最低 {min(soils):.1f}%")
        
    return "\n".join(stats_text)

def get_garden_context(plot_id: int, db: Session) -> str:
    """获取茶园、地块和最新传感器数据的上下文"""
    if not plot_id:
        return "用户未指定具体地块。"

    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    if not plot:
        return f"找不到 ID 为 {plot_id} 的地块。"

    context = [f"当前地块: {plot.name} (ID: {plot.id})"]
    
    # 获取所属茶园信息
    if plot.garden_id:
        garden = db.query(TeaGarden).filter(TeaGarden.id == plot.garden_id).first()
        if garden:
            context.append(f"所属茶园: {garden.name}, 位置: {garden.address or '未知'}")

    # 获取最新传感器数据
    sensor = db.query(SensorRecord).filter(SensorRecord.plot_id == plot_id).order_by(SensorRecord.timestamp.desc()).first()
    if sensor:
        context.append(f"当前最新环境数据 ({sensor.timestamp}):")
        context.append(f"- 土壤湿度: {sensor.soil_moisture}%")
        if sensor.temperature:
            context.append(f"- 空气温度: {sensor.temperature}°C")
        if sensor.humidity:
            context.append(f"- 空气湿度: {sensor.humidity}%")
    else:
        context.append("暂无传感器数据。")
        
    # 获取历史统计数据
    history_stats = get_recent_sensor_stats(plot_id, db)
    if history_stats:
        context.append(history_stats)

    return "\n".join(context)

def generate_chat_response(request: ChatRequest, db: Session) -> str:
    """
    生成聊天回复
    1. 获取知识库内容
    2. 获取地块上下文（如果有）
    3. 构建 Prompt 调用 LLM
    """
    global client
    if not client:
         return "错误：LLM 客户端未初始化。请检查 API Key 配置。"

    try:
        kb_text = get_knowledge_base_content()
        context_text = get_garden_context(request.plot_id, db) if request.plot_id else "无特定地块上下文"
        
        system_prompt = f"""你是一名经验丰富的茶叶农学专家助手。你的任务是根据提供的背景信息和知识库回答用户关于茶园管理、病虫害防治和茶叶种植的问题。

【实时背景信息】
{context_text}

【专业知识库】
{kb_text}

【回答原则】
1. 基于上述信息回答，如果信息不足可以根据通用农业知识补充，但要说明。
2. 回答简洁专业，使用中文。
3. 如果发现传感器数据异常（如土壤过干），请主动提出预警和建议。
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史对话
        if request.history:
            for msg in request.history[-5:]: # 限制历史记录轮数
                messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": request.question})

        response = client.chat.completions.create(
            model=MODEL_NAME, # 使用配置的模型名称
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {e}")
        return "抱歉，我现在无法连接到智能大脑，请稍后再试。(Error: LLM Service Unavailable)"

