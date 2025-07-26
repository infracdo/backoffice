from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import (
    AnyHttpUrl,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    field_validator,
    ValidationInfo
)

class Settings(BaseSettings):

    SECRET: str
    JWT_ALGO: str

    IBM_COS_API_KEY: str
    IBM_COS_SERVICE_INSTANCE_ID: str
    IBM_COS_BUSCKET_NAME: str
    IBM_COS_REGION: str

    MANDRILL_API: str
    MANDRILL_NAME: str
    MANDRILL_EMAIL: str

    MACRODROID_URL: str
    ROUTER_URL: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        data = info.data
        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        host = data.get("POSTGRES_SERVER")
        port = data.get("POSTGRES_PORT")
        db = data.get("POSTGRES_DB")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

settings = Settings()