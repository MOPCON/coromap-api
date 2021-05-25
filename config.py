from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    firebase_url: AnyHttpUrl

    class Config:
        env_file = '.env'
