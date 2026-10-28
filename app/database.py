from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Define the database URL (this creates app.db in your root folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# 2. Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. THIS IS THE MISSING PIECE:
Base = declarative_base()

# 5. The dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()