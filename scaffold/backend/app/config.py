from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # 后端项目的根路径


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_HOURS: int = 24
    JWT_ALGORITHM: str = "HS256"

    # MCP 服务
    MCP_HOST: str = "127.0.0.1"
    MCP_PORT: int = 8001
    MCP_PATH: str = "/mcp"
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_API_KEY: str = ""
    LLM_MODEL_NAME: str = "deepseek-flash"
    # 14 是本节的演示预算：当前简单图为 6 次“模型→工具”往返及最终回答留出步数。
    # 不是框架默认值；增加中间件或改变执行图后，需要重新验证预算
    AGENT_RECURSION_LIMIT: int = 14
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )


settings = Settings()

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100M

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".zip",
}
STUDY_PLAN_MAX_LENGTH = 2000