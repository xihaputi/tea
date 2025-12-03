# app/mqtt_client.py
import json
import threading
# app/mqtt_client.py
import json
import threading
import paho.mqtt.client as mqtt

from .config import settings
from .services.telemetry import save_telemetry  # 你自己实现的入库逻辑

# 订阅所有设备的遥测数据： tea/{tenant}/{farm}/{device}/telemetry
# 订阅所有设备的遥测数据： tea/{device_type}/{sn}/telemetry
SUBSCRIBE_TOPIC = "tea/+/+/telemetry"

client = mqtt.Client(client_id="tea-backend-service")
client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)


def on_connect(client, userdata, flags, rc):
    print("EMQX connected, rc =", rc)
    client.subscribe(SUBSCRIBE_TOPIC, qos=1)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        topic = msg.topic                           # e.g. tea/sensor/SN123456/telemetry
        parts = topic.split("/")
        # parts: ["tea", device_type, sn, "telemetry"]
        if len(parts) < 4:
            print(f"Invalid topic format: {topic}")
            return
            
        _, device_type, sn, _ = parts

        # 调用业务逻辑 / 写数据库
        save_telemetry(sn=sn, data=payload)
        
    except Exception as e:
        print("handle mqtt message error:", e)


client.on_connect = on_connect
client.on_message = on_message


def start_mqtt_loop():
    """在 FastAPI 启动时调用，启动一个后台线程连接 EMQX 并循环收消息"""
    def _loop():
        client.connect(settings.MQTT_HOST, settings.MQTT_PORT, keepalive=60)
        client.loop_forever()

    t = threading.Thread(target=_loop, daemon=True)
    t.start()


def stop_mqtt_loop():
    """关闭 MQTT 客户端（可选调用）"""
    try:
        client.loop_stop()
        client.disconnect()
    except Exception:
        pass


def publish(topic: str, payload: dict, qos: int = 1, retain: bool = False):
    """后端给设备下发 MQTT 消息时用"""
    client.publish(topic, json.dumps(payload), qos=qos, retain=retain)
