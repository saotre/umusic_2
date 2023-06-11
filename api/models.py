from pydantic import BaseSettings, Field



class PostgresDsn(BaseSettings):

    drivername: str = 'postgresql'
    host: str = Field(..., env="DB_HOST")
    port: int = Field(..., env="DB_PORT")
    username: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    database: str = Field(..., env="DB_NAME")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


POSTGRES_DSN = PostgresDsn().dict()
