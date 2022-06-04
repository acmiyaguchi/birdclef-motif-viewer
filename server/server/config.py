from pydantic import BaseSettings


class Settings(BaseSettings):
    static_host: str = "http://localhost:8001"
