from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    tg_token: str = Field(alias='TELEGRAM_TOKEN')

    base_url: str = Field(alias='BASE_URL')
    api_key: str = Field(alias='API_KEY')
    llm_model_name: str = Field(alias='MODEL_NAME')
    temperature: int = Field(alias='TEMPERATURE')
    max_tokens: int = Field(alias='MAX_TOKENS')


settings = Settings()