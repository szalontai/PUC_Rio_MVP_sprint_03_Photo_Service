from flask import Flask, redirect, request, send_file,Response,jsonify,json,send_from_directory
from sqlalchemy import select
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import Session
from logger import logger
from schemas import *
from flask_cors import CORS
from werkzeug.utils import secure_filename
from termcolor import colored
from PIL import Image

import os.path as path
import os
import model
import sqlite3

info = Info(title="Photo Service", version="1.0.0")

app = OpenAPI(__name__, info=info,)
CORS(app)

# Pasta para armazenar as imagens enviadas.
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False

home_tag = Tag(name="Photo Service",description="Documentação da API do Photo Service.")

photo_tag = Tag(name="Fotos",description="Microserviço de gestão de fotos.")

# Página inicial.
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, tela do swagger com a documentação do Photo Service.
    """
    return redirect('/openapi/swagger')

# Faz a inclusão de uma foto.
@app.post('/photo/post', tags=[photo_tag],responses={"200": PhotoViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_photo():
    """Adiciona uma nova foto à base de dados.

    Retorna uma representação da foto.
    """

    # carga dos campos

    _photo_user = request.form['photo_user']
    logger.debug(colored(f"Carregou o id cliente '{_photo_user}'.", 'blue', attrs=['dark']))

    _photo_login = request.form['photo_login']
    logger.debug(colored(f"Carregou o login cliente '{_photo_login}'.", 'blue', attrs=['dark']))

    # tratamento da photo
    _file = request.files['photo_imagem']
    _filename = os.path.join(app.config['UPLOAD_FOLDER'], _file.filename)

    logger.debug(colored(f"Carregou o arquivo de nome '{_file.filename}'.", 'blue', attrs=['dark']))

    _session = Session()

    _cursor_produto = _session.query(Photo).filter(
        Photo.photo_nome == _file.filename and 
        Photo.photo_user == _photo_user).count()

    if _cursor_produto:
        _error_msg = "Foto já cadastrada no banco de dados :/"
        logger.warning(colored(f"Foto já cadastrada no banco de dados ", 'yellow', attrs=['bold']))
        return {"mensagem": _error_msg}, 409

    else:

        # criando conexão com a base
        _sqliteConnection = sqlite3.connect(model.db_name)
        _cursor = _sqliteConnection.cursor()

        try:

            _photo_logradouro = request.form['photo_logradouro']
            logger.debug(colored(f"Carregou photo_logradouro '{_photo_logradouro}'.", 'blue', attrs=['dark']))

            _photo_complemento = request.form['photo_complemento']
            logger.debug(colored(f"Carregou photo_complemento '{_photo_complemento}'.", 'blue', attrs=['dark']))

            _photo_bairro = request.form['photo_bairro']
            logger.debug(colored(f"Carregou photo_bairro '{_photo_bairro}'.", 'blue', attrs=['dark']))

            _photo_localidade = request.form['photo_localidade']
            logger.debug(colored(f"Carregou photo_localidade '{_photo_localidade}'.", 'blue', attrs=['dark']))

            _photo_uf = request.form['photo_uf']
            logger.debug(colored(f"Carregou photo_uf '{_photo_uf}'.", 'blue', attrs=['dark']))

            _photo_cep = request.form['photo_cep']
            logger.debug(colored(f"Carregou photo_cep '{_photo_cep}'.", 'blue', attrs=['dark']))

            logger.debug(colored(
                f"Inicio do proocess.", 'blue', attrs=['dark']))


            logger.debug(colored(
                f"Carregou a pasta '{UPLOAD_FOLDER}' para upload.", 'blue', attrs=['dark']))

            _file.save(_filename)

            logger.debug(colored(
                f"Salvou o  arquivo '{_filename}' para upload.", 'blue', attrs=['dark']))


            # Redimensiona a imagem para uma versão menor
            _image = Image.open(_filename)
            _image.thumbnail((1000, 1000))
            _image.save(_filename)

            logger.debug(colored(f"Salvou o aquivo .", 'blue', attrs=['dark']))
            
            logger.debug(colored(f"Adicionando a foto : '{_filename}'", 'blue', attrs=['dark']))

            _photo_descricao = request.form['photo_descricao']

            logger.debug(colored(f"Carregou a descrição '{_photo_descricao}'.", 'blue', attrs=['dark']))

            # Convertendo a fotopara o formato binário(BLOB)
            _photoBLOB = convertToBinaryData(_filename)

            logger.debug(colored(f"Converteu a fotopara BLOB '{_photo_descricao}'.", 'blue', attrs=['dark']))


            # Convertendo os dados no formato de tuple
            _data_tuple = (_photo_user, _photoBLOB, _file.filename,_photo_descricao,\
                          _photo_logradouro,_photo_complemento,_photo_bairro,\
                          _photo_localidade,_photo_uf,_photo_cep,datetime.now(),_photo_login)

             
            _sqlite_insert_blob_query = """ INSERT INTO photo(
                                                photo_user,photo_imagem,photo_nome,photo_descricao,
                                                photo_logradouro,photo_complemento,photo_bairro,
                                                photo_localidade,photo_uf,photo_cep,photo_data_insercao,photo_login) 
                                            VALUES (?,  ? ,? , ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                        """

            # adicionando a photo
            _cursor.execute(_sqlite_insert_blob_query, _data_tuple)


            logger.debug(colored(f"Fez o insert .", 'blue', attrs=['dark']))


            # efetivando o camando de adição da photo
            _sqliteConnection.commit()

            _photo_requery = _session.query(Photo).filter(
                Photo.photo_nome == _file.filename and Photo.photo_user == _photo_user).first()

            logger.debug(
                colored(f"Adicionado a foto: '{_filename}'", 'green', attrs=['bold']))
            return apresenta_photo(_photo_requery), 200

        except IntegrityError as e:
            _error_msg = "Foto já salva na base :/"
            logger.warning(colored(f"Erro ao adicionar a foto: '{_filename}', {_error_msg}", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto ocorra
            _error_msg = "Não foi possível salvar nova foto:/"
            logger.warning(colored(f"Erro ao adicionar a foto", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 400

        finally:

            _cursor.close()

# Faz a atualização de uma foto.
@app.put('/photo/put', tags=[photo_tag],responses={"200": PhotoViewSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def put_photo():
    """Atualiza uma foto na base de dados.
    
    Retorna uma representação da foto.
    """

    # carga dos campos

    _photo_id = request.form['photo_id']
       
    _session = Session()

    _cursor_photo = _session.query(Photo).filter(Photo.photo_id == _photo_id).count()

    if not _cursor_photo:
        
        logger.warning(colored(f"Foto '{_photo_id}' não cadastrada no banco de dados ", 'yellow', attrs=['bold']))
        _error_msg = "Foto não cadastrada no banco de dados :/"
        return {"mensagem": _error_msg}, 409

    else:

        try:

            _cursor_photo = _session.query(Photo).filter(Photo.photo_id == _photo_id).one()

            _cursor_photo.photo_user=request.form['photo_user']
            _cursor_photo.photo_login=request.form['photo_login']
            _cursor_photo.photo_descricao=request.form['photo_descricao']
            _cursor_photo.photo_logradouro=request.form['photo_logradouro']
            _cursor_photo.photo_complemento=request.form['photo_complemento']
            _cursor_photo.photo_bairro=request.form['photo_bairro']
            _cursor_photo.photo_localidade=request.form['photo_localidade']
            _cursor_photo.photo_uf=request.form['photo_uf']
            _cursor_photo.photo_cep=request.form['photo_cep']

            _session.commit()

            logger.debug(colored(f"Atualizando a foto: '{_photo_id}' ", 'green', attrs=['bold']))
            
            return apresenta_photo(_cursor_photo), 200

        except IntegrityError as e:
            # como a duplicidade do id_imovel e do id_tipo_comodo é a provável razão do IntegrityError
            _error_msg = "Foto já salva na base :/"
            logger.warning(colored(f"Erro ao adicionar a foto: '{_photo_id}' , {_error_msg}", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto ocorra
            _error_msg = "Não foi possível atualizar a foto:/"
            logger.warning(colored(f"Erro ao atualizar a foto'{_photo_id}' ", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 400

# Faz a busca de uma foto.
@app.get('/photo/get', tags=[photo_tag],responses={"200": PhotoResultSchema, "404": ErrorSchema})
def retornar_photo(query: PhotoBuscaSchema):
    """Faz a busca pela foto a partir do id informado.

    Retorna uma representação da foto com os seus comentários .
    """

    # Carga do campo
    _photo_id = query.photo_id

    logger.debug(colored(f"Coletando dados sobre a foto de id# {_photo_id}", 'blue', attrs=['dark']))

   
    session = Session()

    _photo = session.query(Photo).filter(Photo.photo_id == _photo_id).count()

    if _photo:

        # criando conexão com a base
        _sqliteConnection = sqlite3.connect(model.db_name)
        _cursor = _sqliteConnection.cursor()

        try:

            logger.debug(colored(f"Coletando dados sobre a foto de id# {_photo_id}", 'blue', attrs=['dark']))

            _photo_requery = session.query(Photo).filter(Photo.photo_id == _photo_id).first()

        except Exception as e:
            # caso um erro fora do previsto ocorra
            _error_msg = "Não foi possível retornar dados da foto {_photo_id} :/"
            logger.warning(colored(f"Erro ao retornar a foto ", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 400

        finally:

            if _photo_requery:

                _images = []

                # Faz a pesquisa dos comentários da foto
                _sql_fetch_blob_query = """  SELECT  comment.comment_post_id,
                                                    comment.comment_author,
                                                    comment.comment_date,
                                                    comment.comment_date_gmt,
                                                    comment.comment_content
                                            from comment 
                                            where  comment.comment_post_id = ?"""
                _cursor.execute(_sql_fetch_blob_query, (_photo_id,))
                _comments_requery = _cursor.fetchall()

                _result = apresenta_comments(_comments_requery)

                _images={
                        "photo": 
                            {
                                "id": _photo_id,
                                "author": _photo_requery.photo_login,
                                "title": _photo_requery.photo_descricao,
                                "date": _photo_requery.photo_data_insercao,
                                "src": request.url.replace(request.url,request.root_url+app.config['UPLOAD_FOLDER']+"/"+_photo_requery.photo_nome).replace("\\","/"),
                                "photo_logradouro": _photo_requery.photo_logradouro,
                                "photo_complemento": _photo_requery.photo_complemento,
                                "photo_bairro": _photo_requery.photo_bairro,
                                "photo_localidade": _photo_requery.photo_localidade,
                                "photo_uf": _photo_requery.photo_uf,
                                "photo_cep": _photo_requery.photo_cep,
                                "peso": _photo_id,
                                "idade": _photo_id,
                                "acessos": _photo_id,
                                "total_comments": _photo_id
                            },
                            "comments": _result

                        }
                    
        
                logger.debug(colored(f"%d fotos encontradas" %len(_images), 'green', attrs=['bold']))
    
                return  _images, 200

            else:
                # se não há fotos cadastradas
                return {"photo": []}, 404



    else:
        # se o cômodo não foi encontrado
        _error_msg = "Foto não encontrada na base :/"
        logger.warning(colored(f"Foto não encontrada na base", 'red', attrs=['bold']))
        return {"mensagem": _error_msg}, 404

# Faz a busca das fotos pelo usuário, página e total por página.
@app.get('/photos/get', tags=[photo_tag],responses={"200": PhotoResultchema, "404": ErrorSchema})
def get_photos(query: PhotosBuscaSchema):
    """Faz a busca por todas as fotos cadastradas por usuário.

    Retorna uma listagem da representação das fotos de um usuário filtando pela página e total por página.
    """

    # Carga dos campos
    _photo_login = query.photo_login
    _photo_page = query.photo_page
    _photo_total = query.photo_total

    # Montagem do filtro do índice
    _start_index = (_photo_page - 1) * _photo_total
    _end_index = _start_index + _photo_total

    logger.debug(colored(f"Coletando fotos do usuário '{_photo_login}'", 'blue', attrs=['dark']))


    _sqliteConnection = sqlite3.connect(model.db_name)
    _cursor = _sqliteConnection.cursor()

    # Foto :Photo
    try:

        if _photo_login=="0":
            _sql_fetch_blob_query = """  SELECT  Photo.pk_photo_id as Id,
                                                Photo.photo_user,
                                                Photo.photo_imagem,
                                                Photo.photo_nome,
                                                Photo.photo_login,
                                                Photo.photo_descricao,
                                                Photo.photo_data_insercao,
                                                Photo.photo_logradouro,
                                                Photo.photo_complemento,
                                                Photo.photo_bairro,
                                                Photo.photo_localidade,
                                                Photo.photo_uf,
                                                Photo.photo_cep
                                        from Photo 
                                        """
            _cursor.execute(_sql_fetch_blob_query, ())

        else:
            _sql_fetch_blob_query = """  SELECT  Photo.pk_photo_id as Id,
                                                Photo.photo_user,
                                                Photo.photo_imagem,
                                                Photo.photo_nome,
                                                Photo.photo_login,
                                                Photo.photo_descricao,
                                                Photo.photo_data_insercao,
                                                Photo.photo_logradouro,
                                                Photo.photo_complemento,
                                                Photo.photo_bairro,
                                                Photo.photo_localidade,
                                                Photo.photo_uf,
                                                Photo.photo_cep
                                        from Photo 
                                        where  Photo.photo_login = ? 
                                        """
            _cursor.execute(_sql_fetch_blob_query, (_photo_login,))

        _results = _cursor.fetchall()

        _photos = _results[_start_index:_end_index]


    except Exception as e:
        # caso um erro fora do previsto ocorra
        _error_msg = "Não foi possível retornar a foto :/"
        logger.warning(colored(f"Erro ao retornar a foto ", 'red', attrs=['bold']))
        return {"mensagem": _error_msg}, 400

    finally:

        _cursor.close()

        if _photos:

            # photos_adicionadas: Photo = []
            _images = []

            for _form in _photos:

                photo_id, photo_user,photo_imagem,photo_nome,photo_login,photo_descricao,\
                photo_data_insercao,photo_logradouro,photo_complemento,photo_bairro,\
                photo_localidade,photo_uf,photo_cep = _form

                # nome_photo_aux1 = photo_nome.replace(app.config['UPLOAD_FOLDER']+"\\","")

                # file_content_base64 = base64.b64encode(file_content).decode('utf-8')
                _images.append({
                        "id": photo_id,
                        "author": photo_login,
                        "title": photo_descricao,
                        "date": photo_data_insercao,
                        "src": request.url.replace('/photos/get',"/"+app.config['UPLOAD_FOLDER']+"/"+photo_nome).replace("\\","/"),
                        "photo_logradouro": photo_logradouro,
                        "photo_complemento": photo_complemento,
                        "photo_bairro": photo_bairro,
                        "photo_localidade": photo_localidade,
                        "photo_uf": photo_uf,
                        "photo_cep": photo_cep,
                        "peso": photo_id,
                        "idade": photo_id,
                        "acessos": photo_id,
                        "total_comments": photo_id
                    })
                # nome_photo_aux = request.url.replace('/photos/get',"/"+photo_nome)
                # nome_photo_aux1 =photo_nome
         
            logger.debug(colored(f"%d fotos encontradas" %len(_images), 'green', attrs=['bold']))
 
            return Response(json.dumps(_images),
                            status=200,
                            mimetype='application/json')

        else:
            # se não há comodos cadastrados
            return {"photos": []}, 409

# Faz o delete de uma foto.
@app.delete('/photo/delete', tags=[photo_tag],responses={"200": PhotoDelSchema, "404": ErrorSchema})
def del_photo(query: PhotoBuscaSchema):
    """Deleta uma foto a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """

    # Carga do campo
    _photo_id = query.photo_id

    logger.debug(colored(f"Deletando dados da foto de id #{_photo_id}", 'blue', attrs=['dark']))

    # criando conexão com a base
    _session = Session()
   
    _photo = _session.query(Photo).filter(Photo.photo_id == _photo_id).count()

    if _photo:

        # criando conexão com a base
        _sqliteConnection = sqlite3.connect(model.db_name)
        _cursor = _sqliteConnection.cursor()

        try:

            _sql_delete_query = """DELETE from Photo where pk_photo_id = ?"""
            _count = _cursor.execute(_sql_delete_query, (_photo_id,))
            _sqliteConnection.commit()

        except Exception as e:

            # caso um erro fora do previsto ocorra
            _error_msg = "Não foi possível apagar a foto :/"
            logger.warning(colored(f"Erro ao apagar a foto ", 'red', attrs=['bold']))
            return {"mensagem": _error_msg}, 400

        finally:

            _cursor.close()

            if _count:

                logger.debug(colored(f"Deletada foto de id #{_photo}", 'green', attrs=['bold']))

                return {
                    "mensagem": "Foto removida",
                    "photo_id": _photo,
                }
            else:

                # avisa se der erro ao deletar a foto
                _error_msg = "Erro ao deletar a foto :/"
                logger.warning(colored(f"Erro ao deletar a foto de id #'{_photo}'", 'red', attrs=['bold']))
                return {"mensagem": _error_msg}, 404

    else:
        # se a foto não foi encontrada
        _error_msg = "Foto não encontrada na base :/"
        logger.warning(colored(f"Foto não encontrada na base", 'red', attrs=['bold']))
        return {"mensagem": _error_msg}, 404

# Faz o inclusão do comentário da foto.
@app.post('/photo/comment', tags=[photo_tag],responses={"200": CommentResultSchema,  "409": ErrorSchema,  "400": ErrorSchema})
def add_comment(form:CommentSchema):
    """Adiciona um novo comentário à foto na base de dados.

    Retorna uma representação do comentário.
    """

    # Carga dos campos
    _comment_post_id = form.comment_post_id
    _comment_author = form.comment_author
    _comment_content = form.comment_content
    
    # criando conexão com a base
    _sqliteConnection = sqlite3.connect(model.db_name)
    _cursor = _sqliteConnection.cursor()

    try:
        
        # Convertendo os dados no formato de tuple
        _data_tuple = (  _comment_post_id, 
                        _comment_author,
                        _comment_content, 
                        datetime.now(), 
                        datetime.now())

        _sqlite_insert_blob_query = """ INSERT INTO comment
                                        (comment_post_id,
                                        comment_author,
                                        comment_content,
                                        comment_date,
                                        comment_date_gmt) 
                                        VALUES ( ?, ?, ?, ?, ?)
                                    """

        # adicionando a comentário
        _cursor.execute(_sqlite_insert_blob_query, _data_tuple)

        logger.debug(colored(f"Fez o insert .", 'blue', attrs=['dark']))

        # efetivando o camando de adição da photo
        _sqliteConnection.commit()
        
        # Select com o comentário adicionado
        _sql_fetch_blob_query = """  SELECT  comment.comment_post_id,
                                            comment.comment_author,
                                            comment.comment_date,
                                            comment.comment_date_gmt,
                                            comment.comment_content
                                    from comment 
                                    where   comment.comment_post_id = ? and 
                                            comment.comment_author = ? and 
                                            comment.comment_content = ?
                                    """
        _cursor.execute(_sql_fetch_blob_query, (_comment_post_id,_comment_author,_comment_content,))
        _comments_requery = _cursor.fetchall()

        logger.debug(colored(f"Adicionado o comentário. ", 'green', attrs=['bold']))
        return apresenta_comment(_comments_requery), 200

    except IntegrityError as e:
        _error_msg = "Comentário já salvo na base :/"
        logger.warning(colored(f"Erro ao adicionar o comentário , {_error_msg}", 'red', attrs=['bold']))
        return {"mensagem": _error_msg}, 409

    except Exception as e:

        # caso um erro fora do previsto ocorra
        _error_msg = "Não foi possível salvar o novo comentário :/"
        logger.warning(colored(f"Erro ao adicionar o comentário ", 'red', attrs=['bold']))
        return {
                "code": "error",
                "message": _error_msg,
                "data": {
                    "status":403
                },
            }, 400   

    finally:

        _cursor.close()

###################################################################################################
# Funções para tratamento da foto
###################################################################################################

# Faz carga da foto.
@app.route('/upload', methods=['POST'])
def upload():
    # Verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado'

    file = request.files['file']

    # Verifica se o arquivo possui um nome e é uma extensão de imagem válida
    if file.filename == '' or not allowed_file(file.filename):
        return 'Nome de arquivo inválido ou extensão não permitida'

    # Salva o arquivo no servidor
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Redimensiona a imagem para uma versão menor
    image = Image.open(filename)
    image.thumbnail((1000, 1000))
    image.save(filename)

    return 'Upload realizado com sucesso'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Converte dados digitais em formato binário.
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# Verifica se a extensão do arquivo é permitida.
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Converte dados binários para o formato adequado e grava no disco rígido.
def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")
