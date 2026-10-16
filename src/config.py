import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional
import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    gemini_api_key: str
    provider: str = "gemini"
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_output_tokens: int = 2048
    top_p: float = 0.95
    system_prompt: str = ""
    max_history: int = 20


def load_config(config_file: str = "config.yaml", env_file: Optional[str] = None) -> Config:
    env_path = BASE_DIR / (env_file or ".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()

    yaml_path = BASE_DIR / config_file
    data = {}
    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    model_cfg = data.get("model", {})
    system_cfg = data.get("system", {})
    chat_cfg = data.get("chat", {})

    return Config(
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        provider=model_cfg.get("provider", "gemini"),
        model_name=model_cfg.get("name", "gemini-2.5-flash"),
        temperature=float(model_cfg.get("temperature", 0.7)),
        max_output_tokens=int(model_cfg.get("max_output_tokens", 2048)),
        top_p=float(model_cfg.get("top_p", 0.95)),
        system_prompt=system_cfg.get("prompt", ""),
        max_history=int(chat_cfg.get("max_history", 20)),
    )


@lru_cache
def get_settings() -> Config:
    return load_config()
