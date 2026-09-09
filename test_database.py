from sqlalchemy import text

from src.database.connection import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database(), current_user;"))
    print(result.fetchone())