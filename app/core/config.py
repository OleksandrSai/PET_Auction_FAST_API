from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR.joinpath(".env")


class AuthJWT(BaseModel):
    private_key_path: Path = Path("certs") / "jwt-private.pem"
    public_key_path: Path = Path("certs") / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 200


class Settings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str

    db_echo: bool = False

    PROJECT_NAME: str = "PET-project Auction"
    api_v1_prefix: str = "/api/v1"

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ENV_PATH
        extra = "allow"


settings = Settings()
