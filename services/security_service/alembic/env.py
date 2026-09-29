from logging.config import fileConfig
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context

from services.security_service.app.models.security_model import Base


load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        ".env",
    )
)


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


SECURITY_DB_HOST = os.getenv("SECURITY_DB_HOST")
SECURITY_DB_PORT = os.getenv("SECURITY_DB_PORT")
SECURITY_DB_NAME = os.getenv("SECURITY_DB_NAME")
SECURITY_DB_USER = os.getenv("SECURITY_DB_USER")
SECURITY_DB_PASSWORD = os.getenv("SECURITY_DB_PASSWORD")


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{SECURITY_DB_USER}:{SECURITY_DB_PASSWORD}@"
    f"{SECURITY_DB_HOST}:{SECURITY_DB_PORT}/{SECURITY_DB_NAME}"
)


def run_migrations_offline() -> None:
    # Run migrations without opening a database connection.
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Run migrations using a live database connection.
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()