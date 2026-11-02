from pathlib import Path
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # App Info
    app_name: str = "Deep"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Paths
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    leads_dir: Path = BASE_DIR / "data" / "leads"
    sessions_dir: Path = BASE_DIR / "data" / "sessions"
    exports_dir: Path = BASE_DIR / "data" / "exports"
    logs_dir: Path = BASE_DIR / "logs"

    # LLM Settings
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    llm_provider: str = Field(default="gemini", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gemini-2.5-flash", alias="LLM_MODEL")
    ollama_host: str = Field(default="http://localhost:11434", alias="OLLAMA_HOST")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    
    # Fast Inference & Reasoning Engines
    groq_api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    nvidia_nim_api_key: Optional[str] = Field(default=None, alias="NVIDIA_NIM_API_KEY")
    nvidia_nim_model: str = Field(default="meta/llama-3.3-70b-instruct", alias="NVIDIA_NIM_MODEL")
    
    # Treg Open-Source Tool Gateway
    treg_api_key: Optional[str] = Field(default=None, alias="TREG_API_KEY")
    treg_base_url: str = Field(default="http://localhost:4400/v1", alias="TREG_BASE_URL")

    # Delivery Settings
    telegram_bot_token: Optional[str] = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(default=None, alias="TELEGRAM_CHAT_ID")
    
    email_sender: Optional[str] = Field(default=None, alias="EMAIL_SENDER")
    email_password: Optional[str] = Field(default=None, alias="EMAIL_PASSWORD")
    email_receiver: Optional[str] = Field(default=None, alias="EMAIL_RECEIVER")
    
    twilio_account_sid: Optional[str] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_from: Optional[str] = Field(default=None, alias="TWILIO_WHATSAPP_FROM")
    whatsapp_number: Optional[str] = Field(default=None, alias="WHATSAPP_NUMBER")

    # Scraper & Discovery Settings
    google_places_api_key: Optional[str] = Field(default=None, alias="GOOGLE_PLACES_API_KEY")
    use_mock_leads: bool = Field(default=False, alias="USE_MOCK_LEADS")

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.leads_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

settings = AppSettings()
settings.ensure_directories()
