from datetime import datetime
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

<<<<<<< HEAD
<<<<<<< HEAD
from model import Session, Marca, Modelo, Veiculo
=======
from model import Session, Agendamento, Cliente, Profissional, Servico
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
from model import Session, Marca, Modelo, Veiculo
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger,\
                             Redoc ou RapiDoc")

<<<<<<< HEAD
<<<<<<< HEAD
marca_tag = Tag(
    name="Marca", description="Adição, visualização,\
                                    edição e remoção de marcas de veiculos à base")

modelo_tag = Tag(
    name="Modelo", description="Adição, visualização,\
                                    edição e remoção de modelos de marcas de veiculos à base")

veiculo_tag = Tag(
    name="Veiculo", description="Adição, visualização,\
                                    edição e remoção de modelos de veiculos da base")

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
=======
agendamento_tag = Tag(
    name="Agendamento", description="Adição, visualização,\
                                    edição e remoção de agendamento à base")
=======
marca_tag = Tag(
    name="Marca", description="Adição, visualização,\
                                    edição e remoção de marcas de veiculos à base")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0

modelo_tag = Tag(
    name="Modelo", description="Adição, visualização,\
                                    edição e remoção de modelos de marcas de veiculos à base")

veiculo_tag = Tag(
    name="Veiculo", description="Adição, visualização,\
                                    edição e remoção de modelos de veiculos da base")

<<<<<<< HEAD
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite\
       a escolha do estilo de documentação.
    """
    return redirect('/openapi')



# ***************************************************  Metodos do marca do veiculo ***************************************
# Novo registro na tabela marca do veiculo
@app.post('/marca', tags=[marca_tag],
          responses={"201": MarcaViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_marca(form: MarcaSchema):
    """ Adicionar a marca de veículo """
    marca = Marca(
      cod_marca = form.codigo,
      des_nome = form.nome
    )

    logger.debug(f"Adicionando a marca de veículo com o nome '{marca.nom_marca}'")
    try:
        # criando conexão com a base
        session = Session()
<<<<<<< HEAD
<<<<<<< HEAD
        # adicionando  
        session.add(marca)
=======
        # adicionando agendamento
        session.add(agendamento)
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
        # adicionando  
        session.add(marca)
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado a marca do veículo com o nome: '{marca.nom_marca}'")
        return apresenta_marca(marca), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "A marca de veículo com o mesmo nome já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar a marca do veículo com nome ={marca.nom_marca}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar uma nova marca de veículo, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela marca do veiculo
@app.put('/marca', tags=[marca_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_marca(form: MarcaEditSchema):
    """Editar uma marca de veiculojá cadastrado na base """
    codigo_marca = form.codigo
    nome_marca = form.nome

    logger.debug(f"Editando a marca de veículo #{codigo_marca}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo


        marca = session.query(Marca)\
                             .filter(Marca.nom_marca ==  nome_marca
                                and Marca.cod_marca != codigo_marca
                             ).first()

        if marca:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         o mesmo nome!"
            logger.warning(
                f"Erro ao editar a marca com o codigo #{codigo_marca}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_marca == id).update({"nom_marca": nome_marca})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado a marca {nome_marca}")
                return '', 204
            else:
                error_msg = f"A marca com o nome {nome_marca} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar a marca '{nome_marca}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar a marca :/{e.__str__}"
        logger.warning(
            f"Erro ao editar a marca com o nome  #'{nome_marca}', {error_msg}")
        return {"message": error_msg}, 500


<<<<<<< HEAD
<<<<<<< HEAD
# Remoção de um registro de marca de veiculo
@app.delete('/marca', tags=[marca_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_marca(form: MarcaBuscaDelSchema):
    """Exclui uma marca da base de dados através do atributo codigo

    Retorna uma mensagem de exclusão com sucesso.
    """
    codigo = form.codigo
    logger.debug(f"Excluindo a marcaID #{codigo}")
    try:
        # criando conexão com a base
        session = Session()
        
        # fazendo a remoção
        count = session.query(Marca).filter(
            Marca.cod_marca == codigo).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo a marca do veiculo codigo #{codigo}")
            return '', 204
        else:
            # se o   não foi encontrado retorno o codigo http 404
            error_msg = "A marca de veículo não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir a marca de veiculo \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir marca do veiculo :/"
        logger.warning(
            f"Erro ao excluir a marca do veiculo com\
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos as marcas
@app.get('/marcas', tags=[marca_tag],
         responses={"200": ListaMarcasSchema, "500": ErrorSchema})
def get_marcas():
    """Consulta as marcas de veículos

    Retorna uma listagem de representações das marcas de veiculos encontrados.
    """
    logger.debug(f"Consultando as marcas de veículos ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        lista = session.query(Marca).all()

        if not lista:
            # se não há marcas cadastrados
            return {"marcas": []}, 200
        else:
            logger.debug(f"%d marcas de veículos encontrados" %
                         len(lista))
            # retorna a representação de marcas
            return apresenta_lista_marca(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar as marcas de listas :/{str(e)}"
        logger.warning(
            f"Erro ao consultar as marcas dos veículos, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código de marca
@app.get('/marca_id', tags=[marca_tag],
         responses={"200": MarcaViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_marca_id(query: MarcaBuscaDelSchema):
    """Consulta um marca pelo codigo

    Retorna uma representação da marca do veículo
    """

    codigo = query.codigo

    logger.debug(
        f"Consultando a marca por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        marca = session.query(Marca)\
                             .filter(Marca.cod_marca == codigo).first()

        if not marca:
            # se não há   cadastrado
            error_msg = "Marca não encontrado na base :/"
            logger.warning(f"Erro ao buscar a marca de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Marca do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_marca(marca), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}")
        return {"message": error_msg}, 500


# ***************************************************  Metodos do modelo da marca do veiculo ***************************************
# Novo registro na tabela modelo da marca do veiculo
@app.post('/modelo', tags=[modelo_tag],
          responses={"201": ModeloViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_modelo(form: ModeloSchema):
    """ Adicionar o modelo de veículo """
    modelo = Modelo(
      cod_modelo = form.codigo,
      nom_modelo = form.nome
    )

    logger.debug(f"Adicionando o modelo da marca de veículo com o nome '{modelo.nom_modelo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando  
        session.add(modelo)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado a marca do veículo com o nome: '{modelo.nom_modelo}'")
        return apresenta_modelo(modelo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O modelo da marca de veículo com o mesmo nome já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar o modelo da marca do veículo com o nome ={modelo.nom_modelo}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar uma novo modelo da marca de veículo, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela modelo da marca do veiculo
@app.put('/modelo', tags=[modelo_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_modelo(form: ModeloEditSchema):
    """Editar um modelo de veiculojá cadastrado na base """
    codigo_modelo = form.codigo
    nome_modelo = form.nome
    codigo_marca = form.marca_id

    logger.debug(f"Editando a marca de veículo #{codigo_modelo}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo


        modelo = session.query(Modelo)\
                             .filter(Modelo.nom_marca ==  nome_modelo
                                and Modelo.cod_modelo != codigo_modelo
                                and Modelo.cod_marca == codigo_marca
                             ).first()

        if modelo:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         o mesmo nome e marca!"
            logger.warning(
                f"Erro ao editar a marca com o codigo #{codigo_modelo}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_modelo == codigo_modelo).update({"nom_modelo": nome_modelo, "cod_marca": codigo_marca})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado a marca {nome_modelo}")
                return '', 204
            else:
                error_msg = f"A marca com o nome {nome_modelo} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar a marca '{nome_modelo}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar a marca :/{e.__str__}"
        logger.warning(
            f"Erro ao editar a marca com o nome  #'{nome_modelo}', {error_msg}")
        return {"message": error_msg}, 500


# Remoção de um registro de modelo de veiculo
@app.delete('/modelo', tags=[modelo_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_modelo(form: ModeloBuscaDelSchema):
    """Exclui uma modelo da base de dados através do atributo codigo

    Retorna uma mensagem de exclusão com sucesso.
    """
    codigo = form.codigo
    logger.debug(f"Excluindo a marcaID #{codigo}")
=======
# Remoção de um registro de um agendamento  - metodo demonstrado no video do mvp
@app.delete('/agendamento', tags=[agendamento_tag],
=======
# Remoção de um registro de marca de veiculo
@app.delete('/marca', tags=[marca_tag],
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_marca(form: MarcaBuscaDelSchema):
    """Exclui uma marca da base de dados através do atributo codigo

    Retorna uma mensagem de exclusão com sucesso.
    """
<<<<<<< HEAD
    id = form.id
    logger.debug(f"Excluindo o agendamento do Cliente ID #{id}")
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
    codigo = form.codigo
    logger.debug(f"Excluindo a marcaID #{codigo}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:
        # criando conexão com a base
        session = Session()
        
        # fazendo a remoção
<<<<<<< HEAD
<<<<<<< HEAD
        count = session.query(Modelo).filter(
            Modelo.cod_modelo == codigo).delete()
=======
        count = session.query(Agendamento).filter(
            Agendamento.id == id).delete()
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
        count = session.query(Marca).filter(
            Marca.cod_marca == codigo).delete()
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
<<<<<<< HEAD
<<<<<<< HEAD
            logger.debug(f"Excluindo o modelo do veiculo codigo #{codigo}")
            return '', 204
        else:
            # se o   não foi encontrado retorno o codigo http 404
            error_msg = "O modelo de veículo não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir o modelo de veiculo \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir o modelo do veiculo :/"
        logger.warning(
            f"Erro ao excluir o modelo do veiculo com\
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos os modelos
@app.get('/modelos', tags=[modelo_tag],
         responses={"200": ListaModelosSchema, "500": ErrorSchema})
def get_modelos():
    """Consulta os modelos de veículos

    Retorna uma listagem de representações dos modelos de veiculos encontrados.
    """
    logger.debug(f"Consultando os modelos de veículos ")
=======
            logger.debug(f"Excluindo o agendamento do cliente ID #{id}")
=======
            logger.debug(f"Excluindo a marca do veiculo codigo #{codigo}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            return '', 204
        else:
            # se o   não foi encontrado retorno o codigo http 404
            error_msg = "A marca de veículo não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir a marca de veiculo \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir marca do veiculo :/"
        logger.warning(
            f"Erro ao excluir a marca do veiculo com\
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos as marcas
@app.get('/marcas', tags=[marca_tag],
         responses={"200": ListaMarcasSchema, "500": ErrorSchema})
def get_marcas():
    """Consulta as marcas de veículos

    Retorna uma listagem de representações das marcas de veiculos encontrados.
    """
<<<<<<< HEAD
    logger.debug(f"Consultando os clientes ")
>>>>>>> parent of 6fc6a5f (commit inicial)
=======
    logger.debug(f"Consultando as marcas de veículos ")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
<<<<<<< HEAD
<<<<<<< HEAD
        lista = session.query(Modelo).all()

        if not lista:
            # se não há marcas cadastrados
            return {"modelos": []}, 200
        else:
            logger.debug(f"%d modelos de veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_modelo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os modelos :/{str(e)}"
        logger.warning(
            f"Erro ao consultar os modelos dos veículos, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código do modelo
@app.get('/modelo_id', tags=[modelo_tag],
         responses={"200": ModeloViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_modelo_id(query: ModeloBuscaDelSchema):
    """Consulta um modelo pelo codigo

    Retorna uma representação da modelo do veículo
    """

    codigo = query.codigo

    logger.debug(f"Consultando um modelo por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        modelo = session.query(Modelo)\
                             .filter(Modelo.cod_modelo == codigo).first()

        if not modelo:
            # se não há   cadastrado
            error_msg = "Modelo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o modelo de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Modelo do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_modelo(modelo), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}")
        return {"message": error_msg}, 500


# Consulta de modelos que possuam o código da marca 
@app.get('/marca_id', tags=[modelo_tag],
                     responses={"200": ListaModelosSchema, "404": ErrorSchema,
=======
        agendamentos = session.query(Agendamento).all()
=======
        lista = session.query(Marca).all()
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0

        if not lista:
            # se não há marcas cadastrados
            return {"marcas": []}, 200
        else:
            logger.debug(f"%d marcas de veículos encontrados" %
                         len(lista))
            # retorna a representação de marcas
            return apresenta_lista_marca(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar as marcas de listas :/{str(e)}"
        logger.warning(
            f"Erro ao consultar as marcas dos veículos, {error_msg}")
        return {"message": error_msg}, 500


<<<<<<< HEAD
@app.get('/agendamento_id', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema, "404": ErrorSchema,
>>>>>>> parent of 6fc6a5f (commit inicial)
                    "500": ErrorSchema})
def get_modelo_por_id_marca (query: ModeloBuscaPorMarcaSchema):
    """Consulta um modelo pelo codigo da marca

        Retorna uma representação da modelo do veículo
    """

    codigo_marca = query.codigo_marca;    

    logger.debug(f"Consultando os modelos que possuem o codigo de marca= #{codigo_marca} ");

=======
# Consulta por código de marca
@app.get('/marca_id', tags=[marca_tag],
         responses={"200": MarcaViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_marca_id(query: MarcaBuscaDelSchema):
    """Consulta um marca pelo codigo

    Retorna uma representação da marca do veículo
    """

    codigo = query.codigo

    logger.debug(
        f"Consultando a marca por codigo = #{codigo} ")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
<<<<<<< HEAD
        modelos = session.query(Modelo)\
                             .filter(Modelo.cod_marca == codigo_marca);

        if not modelos:
            # se não há   cadastrado
            error_msg = "Modelo não encontrado na base :/"
            logger.warning(f"Erro ao buscar os modelos com o codigo de marca , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Modelo do veículo #{modelos} encontrado");

            # retorna a representação de  s
            return apresenta_lista_modelo(modelos), 200

=======
        marca = session.query(Marca)\
                             .filter(Marca.cod_marca == codigo).first()

        if not marca:
            # se não há   cadastrado
            error_msg = "Marca não encontrado na base :/"
            logger.warning(f"Erro ao buscar a marca de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Marca do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_marca(marca), 200
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    except Exception as e:

        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"
<<<<<<< HEAD

        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}");

=======
        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
        return {"message": error_msg}, 500
                    

<<<<<<< HEAD
# ***************************************************  Metodos do veiculo ***********************************************************************
# Novo registro na tabela veiculo
@app.post('/veiculo', tags=[veiculo_tag],
          responses={"201": VeiculoViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_veiculo(form: VeiculoSchema):
    """ Adicionar o veículo """
    veiculo = Veiculo(
      placa = form.placa,
      codigo_modelo= form.modelo_id
    )

    logger.debug(f"Adicionando o veículo com a placa '{veiculo.des_placa}'")
=======

# ***************************************************  Metodos do modelo da marca do veiculo ***************************************
# Novo registro na tabela modelo da marca do veiculo
@app.post('/modelo', tags=[modelo_tag],
          responses={"201": ModeloViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_modelo(form: ModeloSchema):
    """ Adicionar o modelo de veículo """
    modelo = Modelo(
      cod_modelo = form.codigo,
      nom_modelo = form.nome
    )

    logger.debug(f"Adicionando o modelo da marca de veículo com o nome '{modelo.nom_modelo}'")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:
        # criando conexão com a base
        session = Session()
        # adicionando  
<<<<<<< HEAD
        session.add(veiculo)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado o veículo com a placa: '{veiculo.des_placa}'")
        return apresenta_veiculo(veiculo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O veículo com o mesmo placa e modelo já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar o veículo com a placa = {veiculo.placa}', {error_msg}")
=======
        session.add(modelo)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado a marca do veículo com o nome: '{modelo.nom_modelo}'")
        return apresenta_modelo(modelo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O modelo da marca de veículo com o mesmo nome já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar o modelo da marca do veículo com o nome ={modelo.nom_modelo}', {error_msg}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
<<<<<<< HEAD
        logger.warning(f"Erro ao adicionar uma novo veículo, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela do veiculo
@app.put('/veiculo', tags=[veiculo_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_veiculo(form: VeiculoEditSchema):
    """Editar um veiculojá cadastrado na base """
    codigo = form.codigo
    placa = form.placa
    codigo_modelo = form.modelo_id

    logger.debug(f"Editando o veículo com a placa {placa}")
=======
        logger.warning(f"Erro ao adicionar uma novo modelo da marca de veículo, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela modelo da marca do veiculo
@app.put('/modelo', tags=[modelo_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_modelo(form: ModeloEditSchema):
    """Editar um modelo de veiculojá cadastrado na base """
    codigo_modelo = form.codigo
    nome_modelo = form.nome
    codigo_marca = form.marca_id

    logger.debug(f"Editando a marca de veículo #{codigo_modelo}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo

<<<<<<< HEAD
        veiculo = session.query(Veiculo)\
                             .filter(Veiculo.des_placa ==  placa
                                and Veiculo.cod_modelo != codigo_modelo
                                and Modelo.cod_veiculo == codigo
                             ).first()

        if veiculo:
=======

        modelo = session.query(Modelo)\
                             .filter(Modelo.nom_marca ==  nome_modelo
                                and Modelo.cod_modelo != codigo_modelo
                                and Modelo.cod_marca == codigo_marca
                             ).first()

        if modelo:
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         o mesmo nome e marca!"
            logger.warning(
<<<<<<< HEAD
                f"Erro ao editar o veiculo com a placa {placa}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_veiculo == codigo).update({"des_placa": placa, "cod_modelo":codigo_modelo})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o veiculo {placa}")
                return '', 204
            else:
                error_msg = f"O veiculo com a placa {placa} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar o veiculo com a placa'{placa}', {error_msg}")
=======
                f"Erro ao editar a marca com o codigo #{codigo_modelo}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_modelo == codigo_modelo).update({"nom_modelo": nome_modelo, "cod_marca": codigo_marca})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado a marca {nome_modelo}")
                return '', 204
            else:
                error_msg = f"A marca com o nome {nome_modelo} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar a marca '{nome_modelo}', {error_msg}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar a marca :/{e.__str__}"
        logger.warning(
<<<<<<< HEAD
            f"Erro ao editar o veículo com a placa '{placa}', {error_msg}")
        return {"message": error_msg}, 500


# Remoção de um registro de veiculo
@app.delete('/veiculo', tags=[veiculo_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_veiculo(form: VeiculoBuscaDelSchema):
    """Exclui um registro da base de dados através do atributo codigo
=======
            f"Erro ao editar a marca com o nome  #'{nome_modelo}', {error_msg}")
        return {"message": error_msg}, 500


# Remoção de um registro de modelo de veiculo
@app.delete('/modelo', tags=[modelo_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_modelo(form: ModeloBuscaDelSchema):
    """Exclui uma modelo da base de dados através do atributo codigo
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0

    Retorna uma mensagem de exclusão com sucesso.
    """
    codigo = form.codigo
<<<<<<< HEAD
    logger.debug(f"Excluindo o veiculo do código #{codigo}")
=======
    logger.debug(f"Excluindo a marcaID #{codigo}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
<<<<<<< HEAD
        count = session.query(Veiculo).filter(
            Veiculo.cod_veiculo == codigo).delete()
=======
        count = session.query(Modelo).filter(
            Modelo.cod_modelo == codigo).delete()
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
<<<<<<< HEAD
            logger.debug(f"Excluido o veiculo com o codigo #{codigo}")
            return '', 204
        else:
            # se o registro não for encontrado retorno o codigo http 404
            error_msg = "O veículo não foi encontrado na base"
=======
            logger.debug(f"Excluindo o modelo do veiculo codigo #{codigo}")
            return '', 204
        else:
            # se o   não foi encontrado retorno o codigo http 404
            error_msg = "O modelo de veículo não foi encontrado na base"
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            logger.warning(
                f"Erro ao excluir o modelo de veiculo \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
<<<<<<< HEAD
        error_msg = "Não foi possível excluir o veiculo :/"
        logger.warning(
            f"Erro ao excluir o veiculo com\
=======
        error_msg = "Não foi possível excluir o modelo do veiculo :/"
        logger.warning(
            f"Erro ao excluir o modelo do veiculo com\
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos os modelos
<<<<<<< HEAD
@app.get('/veiculo', tags=[veiculo_tag],
         responses={"200": ListaVeiculosSchema, "500": ErrorSchema})
def get_veiculos():
=======
@app.get('/modelos', tags=[modelo_tag],
         responses={"200": ListaModelosSchema, "500": ErrorSchema})
def get_modelos():
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    """Consulta os modelos de veículos

    Retorna uma listagem de representações dos modelos de veiculos encontrados.
    """
    logger.debug(f"Consultando os modelos de veículos ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
<<<<<<< HEAD
        lista = session.query(Veiculo).all()

        if not lista:
            # se não há marcas cadastrados
            return {"veiculos": []}, 200
        else:
            logger.debug(f"%veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_veiculo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os veiculos :/{str(e)}"
        logger.warning(
            f"Erro ao consultar os veículos, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código de veiculo
@app.get('/veiculo_id', tags=[veiculo_tag],
         responses={"200": ModeloViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_veiculo_id(query: VeiculoBuscaDelSchema):
    """Consulta um veiculo pelo codigo

    Retorna uma representação de  veículo
    """

    codigo = query.codigo

    logger.debug( f"Consultando um veiculo por codigo = #{codigo} ")
=======
        lista = session.query(Modelo).all()

        if not lista:
            # se não há marcas cadastrados
            return {"modelos": []}, 200
        else:
            logger.debug(f"%d modelos de veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_modelo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os modelos :/{str(e)}"
        logger.warning(
            f"Erro ao consultar os modelos dos veículos, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código do modelo
@app.get('/modelo_id', tags=[modelo_tag],
         responses={"200": ModeloViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_modelo_id(query: ModeloBuscaDelSchema):
    """Consulta um modelo pelo codigo

    Retorna uma representação da modelo do veículo
    """

    codigo = query.codigo

    logger.debug(f"Consultando um modelo por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        modelo = session.query(Modelo)\
                             .filter(Modelo.cod_modelo == codigo).first()

        if not modelo:
            # se não há   cadastrado
            error_msg = "Modelo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o modelo de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Modelo do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_modelo(modelo), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}")
        return {"message": error_msg}, 500


# Consulta de modelos que possuam o código da marca 
@app.get('/marca_id', tags=[modelo_tag],
                     responses={"200": ListaModelosSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_modelo_por_id_marca (query: ModeloBuscaPorMarcaSchema):
    """Consulta um modelo pelo codigo da marca

        Retorna uma representação da modelo do veículo
    """

    codigo_marca = query.codigo_marca;    

    logger.debug(f"Consultando os modelos que possuem o codigo de marca= #{codigo_marca} ");

    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        modelos = session.query(Modelo)\
                             .filter(Modelo.cod_marca == codigo_marca);

        if not modelos:
            # se não há   cadastrado
            error_msg = "Modelo não encontrado na base :/"
            logger.warning(f"Erro ao buscar os modelos com o codigo de marca , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Modelo do veículo #{modelos} encontrado");

            # retorna a representação de  s
            return apresenta_lista_modelo(modelos), 200

    except Exception as e:

        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"

        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}");

        return {"message": error_msg}, 500
                    

# ***************************************************  Metodos do veiculo ***********************************************************************
# Novo registro na tabela veiculo
@app.post('/veiculo', tags=[veiculo_tag],
          responses={"201": VeiculoViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_veiculo(form: VeiculoSchema):
    """ Adicionar o veículo """
    veiculo = Veiculo(
      placa = form.placa,
      codigo_modelo= form.modelo_id
    )

    logger.debug(f"Adicionando o veículo com a placa '{veiculo.des_placa}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando  
        session.add(veiculo)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado o veículo com a placa: '{veiculo.des_placa}'")
        return apresenta_veiculo(veiculo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O veículo com o mesmo placa e modelo já foi salvo anteriormente na base :/"
        logger.warning(
            f"Erro ao adicionar o veículo com a placa = {veiculo.placa}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar uma novo veículo, {error_msg}")
        return {"message": error_msg}, 400


# Edicao registro na tabela do veiculo
@app.put('/veiculo', tags=[veiculo_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_veiculo(form: VeiculoEditSchema):
    """Editar um veiculojá cadastrado na base """
    codigo = form.codigo
    placa = form.placa
    codigo_modelo = form.modelo_id

    logger.debug(f"Editando o veículo com a placa {placa}")
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
    try:

        # criando conexão com a base
        session = Session()
<<<<<<< HEAD
        # fazendo a busca
        veiculo = session.query(Veiculo)\
                             .filter(Veiculo.cod_veiculo == codigo).first()

        if not veiculo:
            # se não há registro cadastrado
            error_msg = "Veiculo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o modelo de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Modelo do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_veiculo(veiculo), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o veículo, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por todos os veículos por código de modelo
@app.get('/modelo_id', tags=[veiculo_tag],
        responses={"200": ListaVeiculosSchema, 
                   "404": ErrorSchema,
                   "500": ErrorSchema})
def get_lista_veiculos_por_id_marca(query: VeiculoBuscaPorModelo):
    """ Consulta de veiculos pelo codigo do modelo

        Retorna uma representação de  veículo
    """

    codigo_modelo = query.codigo_modelo;

    logger.debug( f"Consultando um veiculo por codigo = #{codigo_modelo} ")

    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        lista = session.query(Veiculo)\
                             .filter(Veiculo.cod_modelo == codigo_modelo).first()

        if not lista:
            # se não há marcas cadastrados
            return {"veiculos": []}, 200
        else:
            logger.debug(f"%veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_veiculo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os veiculos :/{str(e)}"
        logger.warning(
=======
        # Consulta se ja existe a descricao com outro codigo

        veiculo = session.query(Veiculo)\
                             .filter(Veiculo.des_placa ==  placa
                                and Veiculo.cod_modelo != codigo_modelo
                                and Modelo.cod_veiculo == codigo
                             ).first()

        if veiculo:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         o mesmo nome e marca!"
            logger.warning(
                f"Erro ao editar o veiculo com a placa {placa}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_veiculo == codigo).update({"des_placa": placa, "cod_modelo":codigo_modelo})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o veiculo {placa}")
                return '', 204
            else:
                error_msg = f"O veiculo com a placa {placa} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar o veiculo com a placa'{placa}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar a marca :/{e.__str__}"
        logger.warning(
            f"Erro ao editar o veículo com a placa '{placa}', {error_msg}")
        return {"message": error_msg}, 500


# Remoção de um registro de veiculo
@app.delete('/veiculo', tags=[veiculo_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_veiculo(form: VeiculoBuscaDelSchema):
    """Exclui um registro da base de dados através do atributo codigo

    Retorna uma mensagem de exclusão com sucesso.
    """
    codigo = form.codigo
    logger.debug(f"Excluindo o veiculo do código #{codigo}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Veiculo).filter(
            Veiculo.cod_veiculo == codigo).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluido o veiculo com o codigo #{codigo}")
            return '', 204
        else:
            # se o registro não for encontrado retorno o codigo http 404
            error_msg = "O veículo não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir o modelo de veiculo \
                 codigo #'{codigo}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir o veiculo :/"
        logger.warning(
            f"Erro ao excluir o veiculo com\
            o codigo #'{codigo}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos os modelos
@app.get('/veiculo', tags=[veiculo_tag],
         responses={"200": ListaVeiculosSchema, "500": ErrorSchema})
def get_veiculos():
    """Consulta os modelos de veículos

    Retorna uma listagem de representações dos modelos de veiculos encontrados.
    """
    logger.debug(f"Consultando os modelos de veículos ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        lista = session.query(Veiculo).all()

        if not lista:
            # se não há marcas cadastrados
            return {"veiculos": []}, 200
        else:
            logger.debug(f"%veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_veiculo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os veiculos :/{str(e)}"
        logger.warning(
            f"Erro ao consultar os veículos, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por código de veiculo
@app.get('/veiculo_id', tags=[veiculo_tag],
         responses={"200": ModeloViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_veiculo_id(query: VeiculoBuscaDelSchema):
    """Consulta um veiculo pelo codigo

    Retorna uma representação de  veículo
    """

    codigo = query.codigo

    logger.debug( f"Consultando um veiculo por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        veiculo = session.query(Veiculo)\
                             .filter(Veiculo.cod_veiculo == codigo).first()

        if not veiculo:
            # se não há registro cadastrado
            error_msg = "Veiculo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o modelo de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Modelo do veículo #{codigo} encontrado")
            # retorna a representação de  s
            return apresenta_veiculo(veiculo), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o veículo, {error_msg}")
        return {"message": error_msg}, 500


# Consulta por todos os veículos por código de modelo
@app.get('/modelo_id', tags=[veiculo_tag],
        responses={"200": ListaVeiculosSchema, 
                   "404": ErrorSchema,
                   "500": ErrorSchema})
def get_lista_veiculos_por_id_marca(query: VeiculoBuscaPorModelo):
    """ Consulta de veiculos pelo codigo do modelo

        Retorna uma representação de  veículo
    """

    codigo_modelo = query.codigo_modelo;

    logger.debug( f"Consultando um veiculo por codigo = #{codigo_modelo} ")

    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        lista = session.query(Veiculo)\
                             .filter(Veiculo.cod_modelo == codigo_modelo).first()

        if not lista:
            # se não há marcas cadastrados
            return {"veiculos": []}, 200
        else:
            logger.debug(f"%veículos encontrados" %
                         len(lista))
            # retorna a representação de modelos
            return apresenta_lista_veiculo(lista), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os veiculos :/{str(e)}"
        logger.warning(
>>>>>>> 081d82a12f484aa04136e06fdeb63577cd3c85d0
            f"Erro ao consultar os veículos, {error_msg}")
        return {"message": error_msg}, 500
