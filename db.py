from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///gitlab.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)


def get_session():
    """Return a new SQLAlchemy session."""
    Base.metadata.create_all(bind=engine)
    return SessionLocal()
