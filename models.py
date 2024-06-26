from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, MEDIUMTEXT, SMALLINT, TEXT, TINYINT, VARCHAR, YEAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EmailData(Base):
    __tablename__ = "email_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(255))
    from_email = Column(Text)
    subject = Column(Text)
    message = Column(Text)
    received_date = Column(DateTime)
    is_read = Column(TINYINT(1))
    is_processed = Column(TINYINT(1), default='INBOX')
    folder = Column(Text)

