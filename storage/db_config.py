import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
print("ENV DEBUG → DB_PASSWORD:", os.getenv("DB_PASSWORD"))

def get_all_db_configs():
    db_list_env = os.getenv("DB_LIST")

    if not db_list_env:
        raise ValueError("DB_LIST not found in .env")

    db_list = [db.strip() for db in db_list_env.split(",")]

    common_config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    # Validate common config
    if not all(common_config.values()):
        raise ValueError("Missing DB connection details in .env")

    configs = []

    for db_name in db_list:
        config = {
            "name": db_name,
            "database": db_name,
            **common_config
        }
        configs.append(config)

    return configs