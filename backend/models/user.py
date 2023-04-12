from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=False)
    last_name = Column(String(255), nullable=False, unique=False)
    mail = Column(String(255), nullable=False, unique=False)
    password = Column(String(255), unique=False, nullable=False)
    active_status = Column(Boolean(), default = False, nullable=False)
    user_data = relationship("UserData")


class UserData(Base):
    __tablename__ = "user_data"

    data_id = Column(Integer, primary_key=True)
    identifier = Column(
        Integer, ForeignKey("user.user_id"), nullable=False, unique=False)
    tax_filing = Column(String(255), nullable=False, unique=False)
    wages = Column(Integer, nullable=False, unique=False)
    total_deduction = Column(Integer, default=True, nullable=False)
    user = relationship("User", back_populates="user_data")