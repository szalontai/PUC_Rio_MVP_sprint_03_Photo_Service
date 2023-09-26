from sqlalchemy import BLOB, Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column("pk_comment_id", Integer, primary_key=True)
    comment_post_id = Column(Integer,nullable=False)
    comment_author = Column(String(20),unique=False,nullable=False)
    comment_content = Column(String(100))
    comment_author_email = Column(String(100))
    comment_author_url = Column(String(100))
    comment_author_IP = Column(String(100))
    comment_date = Column(DateTime, default=datetime.now())
    comment_date_gmt = Column(DateTime, default=datetime.now())
    comment_karma = Column(String(100))
    comment_approved = Column(String(100))
    comment_agent = Column(String(100))
    comment_type = Column(String(100))
    comment_parent = Column(String(100))
    user_id = Column(Integer)
  
    def __init__(self,
                 comment_post_id:int,
                 comment_author:str, 
                 comment_author_email:str, 
                 comment_author_url:str, 
                 comment_author_IP:str, 
                 comment_content:str, 
                 comment_karma:str, 
                 comment_approved:str, 
                 comment_agent:str, 
                 comment_type:str, 
                 comment_parent:str, 
                 user_id:int, 
                 comment_date:Union[DateTime, None] = None, 
                 comment_date_gmt:Union[DateTime, None] = None
                 ):

        self.comment_post_id = comment_post_id
        self.comment_author = comment_author
        self.comment_author_email = comment_author_email
        self.comment_author_url = comment_author_url
        self.comment_author_IP = comment_author_IP
        self.comment_content = comment_content
        self.comment_karma = comment_karma
        self.comment_approved = comment_approved
        self.comment_agent = comment_agent
        self.comment_type = comment_type
        self.comment_parent = comment_parent
        self.user_id = user_id

        if comment_date:
            self.comment_date = comment_date
        if comment_date_gmt:
            self.comment_date_gmt = comment_date_gmt
