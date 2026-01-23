from sqlalchemy import create_engine
from etl.config.settings import (
    DB_HOST, DB_PORT, DB_NAME,
    DB_USER, DB_PASSWORD, DB_SCHEMA
)

def get_engine():
    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD não foi carregada do .env")

    url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(
        url,
        connect_args={"options": f"-csearch_path={DB_SCHEMA}"}
    )

    return engine