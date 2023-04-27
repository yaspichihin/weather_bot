class Settings:
    weather_yandex_key: str = ...
    geocoder_yandex_key: str = ...

    db_host: str = ...
    db_port: str = ...
    db_user: str = ...
    db_pass: str = ...
    db_name: str = ...

    # Telegram id администраторов
    tg_bot_admin: list[int] = [..., ]

    telegram_key: str = ...

    @property
    def database_url(self):
        user = f"{self.db_user}:{self.db_pass}"
        db = f"{self.db_host}:{self.db_port}/{self.db_name}"
        return f"postgresql+asyncpg://{user}@{db}"


settings = Settings()