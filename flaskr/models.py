from database import Base
from sqlalchemy import Column, Integer, String, Boolean

'''
class Signups(Base):
    """
    Example Signups table
    """
    __tablename__ = 'destination'
    id = Column(Integer, primary_key=True)
    address_show_txt = Column(String)

'''


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False)
    is_driver = Column(Boolean, default=False)
    will_present = Column(Boolean, default=False)
    capacity = Column(Integer, default=1)
    phone_number = Column(String, default="N/A")
    address_id = Column(String)
    address_show_txt = Column(String)
