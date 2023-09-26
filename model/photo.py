from sqlalchemy import BLOB, Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class Photo(Base):
    __tablename__ = 'photo'

    photo_id = Column("pk_photo_id", Integer, primary_key=True)
    photo_user = Column(Integer,nullable=False)
    photo_login = Column(String(20),unique=False,nullable=False)
    photo_nome = Column(String(4000),nullable=False)  
    photo_imagem = Column(BLOB,nullable=False)  
    photo_descricao =  Column(String(4000))  
    photo_logradouro =  Column(String(100))  
    photo_complemento =  Column(String(50))  
    photo_bairro =  Column(String(100))  
    photo_localidade =  Column(String(100))  
    photo_uf =  Column(String(2))  
    photo_cep =  Column(String(10))  

    photo_data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self,photo_user:int,photo_imagem:BLOB,photo_nome:str, photo_login:str, 
                 photo_descricao:str,photo_logradouro:str,photo_complemento:str, 
                 photo_bairro:str, photo_localidade:str, photo_uf:str,  photo_cep:str,  
                 photo_data_insercao:Union[DateTime, None] = None):

        self.photo_user = photo_user
        self.photo_login = photo_login
        self.photo_imagem = photo_imagem
        self.photo_nome = photo_nome
        self.photo_descricao = photo_descricao
        self.photo_logradouro = photo_logradouro
        self.photo_complemento = photo_complemento
        self.photo_bairro = photo_bairro
        self.photo_localidade = photo_localidade
        self.photo_uf = photo_uf
        self.photo_cep = photo_cep

        if photo_data_insercao:
            self.photo_data_insercao = photo_data_insercao
