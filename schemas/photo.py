from pydantic import BaseModel 
from typing import List
from model.photo import Photo
from model.comment import Comment
from datetime import datetime

class CommentSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a inclusão de um comentário. 
    """

    comment_post_id: int = 0
    comment_author: str = "comment_author"
    comment_content: str = "comment_content"

class CommentResultSchema(BaseModel):
    """ Define como deve ser a estrutura que retorna um comentário. 
    """

    comment_post_ID: int 
    comment_author: str 
    comment_date: str 
    comment_date_gmt: datetime 
    comment_content: datetime 

class PhotoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de uma foto. 
        Será feita apenas com base no photo_id da foto.
    """
    photo_id: int = 0  # Id da foto

class PhotosBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca das fotos de um usuário. 
        Será feita apenas com base na photo_login, photo_page e photo_total da foto.
    """
    photo_login: str  # Id da foto
    photo_page: int = 0  # Id da foto
    photo_total: int = 0  # Id da foto

class PhotoViewSchema(BaseModel):
    """ Define como uma foto da será retornada.
    """
    photo_id: int
    photo_user: int
    photo_nome: str
    photo_descricao: str
    photo_login: str  
    photo_logradouro: str  
    photo_complemento: str  
    photo_bairro: str  
    photo_localidade: str  
    photo_uf: str  
    photo_cep: str  
   
class PhotoResultchema(BaseModel):
    """ Define como uma foto será retornada.
    """

    id: int
    author: str
    title: str
    date: str
    src: str
    photo_logradouro: str
    photo_complemento: str
    photo_bairro: str
    photo_localidade: str
    photo_uf: str
    photo_cep: str
    peso: int
    idade: int
    acessos: int
    total_comments: str
    
class PhotoItemSchema(BaseModel):
    """ Define como uma foto e os comentários será retornada.
    """

    id: int
    author: str
    title: str
    date: str
    src: str
    photo_logradouro: str
    photo_complemento: str
    photo_bairro: str
    photo_localidade: str
    photo_uf: str
    photo_cep: str
    peso: int
    idade: int
    acessos: int
    total_comments: str
    comments :CommentResultSchema
    
class PhotoResultSchema(BaseModel):
    """ Define como uma foto e os seus comentários será retornada.
    """

    photo: PhotoItemSchema
    
class PhotoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma exclusão
        de remoção.
    """
    mensagem: str = "Foto removida"
    photo_id: int

def apresenta_photo(photo: Photo):
    """ Retorna uma representação da foto.
    """
 
    result = {
        "photo_id": photo.photo_id,
        "photo_user": photo.photo_user,
        "photo_login": photo.photo_login,
        "photo_nome": photo.photo_nome,
        "photo_descricao": photo.photo_descricao,
        "photo_logradouro": photo.photo_logradouro,
        "photo_complemento": photo.photo_complemento,
        "photo_bairro": photo.photo_bairro,
        "photo_localidade": photo.photo_localidade,
        "photo_uf": photo.photo_uf,
        "photo_cep": photo.photo_cep,
        "photo_data_insercao": photo.photo_data_insercao,
    }

    return result

def apresenta_photos(s_photo: List[Photo]):
    """ Retorna uma listagem da representação da foto.
    """

    _result = []

    for _photo in s_photo:

        # print("Passou aqui 2")
        _result.append(
            {
                "photo_id": _photo["photo_id"],
                "photo_nome": _photo["photo_nome"],
                "photo_login": _photo["photo_login"],
                "photo_user": _photo["photo_user"],
                "photo_nome": _photo["photo_nome"],
                "photo_descricao": _photo["photo_descricao"],
                "photo_logradouro": _photo["photo_logradouro"],
                "photo_complemento": _photo["photo_complemento"],
                "photo_bairro": _photo["photo_bairro"],
                "photo_uf": _photo["photo_uf"],
                "photo_cep": _photo["photo_cep"],
                "photo_data_insercao": _photo["photo_data_insercao"],
            }
        )

    return {"": _result}

def apresenta_comment(comment: Comment):
    """ Retorna a representação do comentário da foto.
    """
    _result = {
                "comment_post_ID": comment[0][0],
                "comment_author": comment[0][1],
                "comment_date": comment[0][2],
                "comment_date_gmt": comment[0][3],
                "comment_content": comment[0][4]
            }

    return _result

def apresenta_comments(comments: List[Comment]):
    """ Retorna uma lista da representação do comentário da foto.
    """
 
    _result = []

    for _comment in comments:

        _result.append(
            {
                "comment_post_id": _comment[0],
                "comment_author": _comment[1],
                "comment_date": _comment[2],
                "comment_date_gmt": _comment[3],
                "comment_content": _comment[4],
            }
        )

    return _result
