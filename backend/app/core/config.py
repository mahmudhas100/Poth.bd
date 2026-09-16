import os
from typing import List, Union
from pydantic import BaseModel, field_validator

class Settings(BaseModel):
    PROJECT_NAME: str = "Poth Transit API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = ""
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: List[str] = ["*"]
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DB_PATH: str = os.getenv("DB_PATH", os.path.join(BASE_DIR, "data", "busvara.db"))

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

cors_env = os.getenv("CORS_ORIGINS")
settings = Settings(
    CORS_ORIGINS=cors_env.split(",") if cors_env else ["*"]
)

