import os
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Use DATABASE_URL environment variable; if not set, default to SQLite.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
