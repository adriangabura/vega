from pathlib import Path

from pydantic import BaseSettings


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    class Config:
        env_file = f"{get_project_root()}/.env"

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    BUCKET_NAME: str
    PRESIGNED_URL_EXPIRATION: int


config = Settings()
