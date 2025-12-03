from pydantic import BaseSettings


class Settings(BaseSettings):

    #数据库配置
    DATABASE_URL: str = "sqlite:///./tea_garden.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UPLOAD_DIR: str = "uploads"

    MQTT_HOST: str = "127.0.0.1"   # EMQX 所在机器 IP
    MQTT_PORT: int = 1883          # 默认 MQTT 端口
    MQTT_USERNAME: str = "admin" # 在 EMQX 中创建的客户端用户名
    MQTT_PASSWORD: str = "public"# 在 EMQX 中创建的客户端密码

    class Config:
        env_file = ".env"


settings = Settings()
