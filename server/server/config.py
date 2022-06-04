from pydantic import BaseSettings


class Settings(BaseSettings):
    static_internal_host: str = "http://static:8000"
    static_external_host: str = "http://localhost:8001"
