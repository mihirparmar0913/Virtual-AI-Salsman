from sqlalchemy import inspect

from src.database.connection import engine
from src.database.models import Product


inspector = inspect(engine)

columns = inspector.get_columns(Product.__tablename__)

print("Products table columns:")

for column in columns:
    print(f"- {column['name']}: {column['type']}")