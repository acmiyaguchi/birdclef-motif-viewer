from pydantic import BaseSettings


class Settings(BaseSettings):
    static_internal_host: str = "http://nginx:4000"
    static_external_host: str = "http://localhost:4000"
