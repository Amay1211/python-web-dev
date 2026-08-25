from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from .config import settings

# SQLALCHEMY_DATABASE_URL is the connection string for the database use to connect to the database
# format: postgresql://<username>:<password>@<host>:<port>/<database_name>
# here postgres is the username, admin is the password, localhost is the host, 5432 is the port, pythonwebdev is the database name

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/pythonwebdev'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

url = URL.create(
    "postgresql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_hostname,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
