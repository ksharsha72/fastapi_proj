from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env",), case_sensitive=False)
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_user: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str


settings = Settings(_env_file="../.env")
