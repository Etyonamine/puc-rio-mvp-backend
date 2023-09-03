from datetime import datetime
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Marca, Modelo, Agendamento, Cliente, Profissional, Servico
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

marca_tag = Tag(
    name="Marca", description="Adição, visualização,\
                                    edição e remoção de marcas de veiculos à base")

modelo_tag = Tag(
    name="Modelo", description="Adição, visualização,\
                                    edição e remoção de modelos de marcas de veiculos à base")


agendamento_tag = Tag(
    name="Agendamento", description="Adição, visualização,\
                                    edição e remoção de agendamento à base")

cliente_tag = Tag(
    name="Cliente", description="Adição, visualização,\
                                 edição e remoção de clientes à base")

profissional_tag = Tag(
    name="Profissional", description="Adição, visualização,\
                                      edição e remoção de profissional à base")
servico_tag = Tag(
    name="Servico", description="Adição, visualização,\
                                 edição e remoção de serviços à base")


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
        # adicionando agendamento
        session.add(marca)
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
            # se o agendamento não foi encontrado retorno o codigo http 404
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
def get_agendamento_id(query: MarcaBuscaDelSchema):
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
            # se não há agendamento cadastrado
            error_msg = "Marca não encontrado na base :/"
            logger.warning(f"Erro ao buscar a marca de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Marca do veículo #{codigo} encontrado")
            # retorna a representação de agendamentos
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
        # adicionando agendamento
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

    logger.debug(f"Editando a marca de veículo #{codigo_modelo}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo


        modelo = session.query(Modelo)\
                             .filter(Modelo.nom_marca ==  nome_modelo
                                and Modelo.cod_marca != codigo_modelo
                             ).first()

        if modelo:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro registro com\
                         o mesmo nome!"
            logger.warning(
                f"Erro ao editar a marca com o codigo #{codigo_modelo}, {error_msg}")
            return {"message": error_msg}, 400
        else:            
            count = session.query(Marca).filter(
                Marca.cod_marca == id).update({"nom_marca": nome_modelo})
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
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Modelo).filter(
            Modelo.cod_modelo == codigo).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o modelo do veiculo codigo #{codigo}")
            return '', 204
        else:
            # se o agendamento não foi encontrado retorno o codigo http 404
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
def get_marcas():
    """Consulta os modelos de veículos

    Retorna uma listagem de representações dos modelos de veiculos encontrados.
    """
    logger.debug(f"Consultando os modelos de veículos ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
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



# Consulta por código de marca
@app.get('/modelo_id', tags=[modelo_tag],
         responses={"200": ModeloViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento_id(query: ModeloBuscaDelSchema):
    """Consulta um modelo pelo codigo

    Retorna uma representação da modelo do veículo
    """

    codigo = query.codigo

    logger.debug(
        f"Consultando um modelo por codigo = #{codigo} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        modelo = session.query(Modelo)\
                             .filter(Modelo.cod_modelo == codigo).first()

        if not modelo:
            # se não há agendamento cadastrado
            error_msg = "Modelo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o modelo de veículo , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Modelo do veículo #{codigo} encontrado")
            # retorna a representação de agendamentos
            return apresenta_modelo(modelo), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar a marca do veículo :/{str(e)}"
        logger.warning(
            f"Erro ao consultar a marca do veículo, {error_msg}")
        return {"message": error_msg}, 500






# Remoção de um registro de um agendamento  - metodo demonstrado no video do mvp
@app.delete('/agendamento', tags=[agendamento_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_agendamento(form: AgendamentoBuscaDelSchema):
    """Exclui um agendamento da base de dados com o codigo id

    Retorna uma mensagem de exclusão com sucesso.
    """
    id = form.id
    logger.debug(f"Excluindo o agendamento do Cliente ID #{id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Agendamento).filter(
            Agendamento.id == id).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o agendamento do cliente ID #{id}")
            return '', 204
        else:
            # se o agendamento não foi encontrado retorno o codigo http 404
            error_msg = "O Agendamento não foi encontrado na base"
            logger.warning(
                f"Erro ao excluir o agendamento do cliente do\
                 ID #'{id}', {error_msg}")
            return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir o agendamento do cliente :/"
        logger.warning(
            f"Erro ao excluir o agendamento do cliente com\
            ID #'{id}', {error_msg}")
        return {"message": error_msg}, 500


# Consulta de todos os agendamentos -  metodo demonstrado no video do mvp
@app.get('/agendamentos', tags=[agendamento_tag],
         responses={"200": ListagemAgendamentoSchema, "500": ErrorSchema})
def get_agendamentos():
    """Consulta os agendamentos dos clientes

    Retorna uma listagem de representações dos clientes encontrados.
    """
    logger.debug(f"Consultando os clientes ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamentos = session.query(Agendamento).all()

        if not agendamentos:
            # se não há agendamentos cadastrados
            return {"agendamentos": []}, 200
        else:
            logger.debug(f"%d agendamentos dos clientes encontrados" %
                         len(agendamentos))
            # retorna a representação de agendamentos
            return apresenta_agendamentos(agendamentos), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os agendamentos :/{str(e)}"
        logger.warning(
            f"Erro ao consultar os agendamentos dos clientes, {error_msg}")
        return {"message": error_msg}, 500


@app.get('/agendamento_id', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento_id(query: AgendamentoBuscaIdSchema):
    """Consulta um agendamento pelo codigo do agendamento

    Retorna uma representação do agendamento do cliente
    """
    id = query.id
    logger.debug(
        f"Consultando o agendamento por id = #{id} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamento = session.query(Agendamento)\
                             .filter(Agendamento.id == id).first()

        if not agendamento:
            # se não há agendamento cadastrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar o agendamento , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Agendamento do cliente ID #{id} encontrado")
            # retorna a representação de agendamentos
            return apresenta_agendamento(agendamento), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o agendamento :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o agendamento do cliente, {error_msg}")
        return {"message": error_msg}, 500


@app.get('/agendamento', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema, "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento(query: AgendamentoBuscaSchema):
    """Consulta um agendamento pela data de agendamento e codigo do cliente

    Retorna uma representação do agendamento do cliente
    """
    cliente_id = query.cliente_id
    data_agenda = datetime.strptime(query.data_agenda, "%d/%m/%Y %H:%M:%S")
    logger.debug(
        f"Consultando o cliente id = {cliente_id} , data = {data_agenda} ")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamento = session.query(Agendamento)\
                             .filter(Agendamento.data_agenda ==
                                     data_agenda).\
            filter(Agendamento.cliente_id == cliente_id).first()

        print(data_agenda)

        if not agendamento:
            # se não há agendamento cadastrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar o agendamento , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Agendamento do cliente ID #{cliente_id}\
                e data de agenda {data_agenda} encontrado")
            # retorna a representação de agendamentos
            return apresenta_agendamento(agendamento), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o agendamento :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o agendamento do cliente, {error_msg}")
        return {"message": error_msg}, 500


@app.get('/agendamento_cliente', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento_cliente(query: AgendamentoBuscaClienteSchema):
    """ Consulta um codigo de cliente se existe alguma agendamento

    Retorna uma representação do primeiro agendamento encontrato
    """
    cliente_id = query.cliente_id
    logger.debug(
        f"Consultando o cliente id = {cliente_id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamento = session.query(Agendamento).filter(
            Agendamento.cliente_id == cliente_id).first()

        if not agendamento:
            # se não há agendamento cadastrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar o agendamento , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Agendamento do cliente ID #{cliente_id}  encontrado")
            # retorna a representação de agendamentos
            return apresenta_agendamento(agendamento), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o agendamento :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o agendamento do cliente, {error_msg}")
        return {"message": error_msg}, 500


@app.get('/agendamento_profissional', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento_profissional(query: AgendamentoBuscaProfissionalSchema):
    """ Consulta um codigo do profissional se existe algum agendamento

    Retorna uma representação do primeiro agendamento encontrato
    """
    id = query.profissional_id
    logger.debug(
        f"Consultando o profissional id = {id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamento = session.query(Agendamento).filter(
            Agendamento.profissional_id == id).first()

        if not agendamento:
            # se não há agendamento cadastrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar o agendamento , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Agendamento do profissional ID #{id}  encontrado")
            # retorna a representação de agendamentos
            return apresenta_agendamento(agendamento), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o agendamento :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o agendamento do cliente, {error_msg}")

        return {f"message: {error_msg}"}, 500


@app.get('/agendamento_servico', tags=[agendamento_tag],
         responses={"200": AgendamentoViewSchema,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def get_agendamento_servico(query: AgendamentoBuscaServicoSchema):
    """ Consulta um codigo do profissional se existe algum agendamento

        Retorna uma representação do primeiro agendamento encontrato
    """
    id = query.servico_id
    logger.debug(f"Consultando o servico id = {id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        agendamento = session.query(Agendamento)\
                             .filter(Agendamento.servico_id == id)\
                             .first()

        if not agendamento:
            # se não há agendamento cadastrado
            error_msg = "Agendamento não encontrado na base :/"
            logger.warning(f"Erro ao buscar o agendamento , {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(
                f"Agendamento do servico ID #{id}  encontrado")
            # retorna a representação de agendamentos
            return apresenta_agendamento(agendamento), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar o agendamento :/{str(e)}"
        logger.warning(
            f"Erro ao consultar o agendamento do cliente, {error_msg}")
        return {"message": error_msg}, 500


# ***************************************************  Metodos do Cliente ***************************************
@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema,
                     "500": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo cliente à base de dados

    Retorna uma representação do cliente.
    """
    cliente = Cliente(
        nome=form.nome.strip()
    )
    logger.debug(f"Adicionando cliente de nome: '{cliente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente de nome: '{cliente.nome}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já cadastrado na base de dados!"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 500


@app.put('/cliente', tags=[cliente_tag],
         responses={"204": None, "400": ErrorSchema,
                    "404": None, "500": ErrorSchema})
def put_cliente(form: ClienteViewSchema):
    """Edita um cliente já cadastrado na base de dados

    Retorna uma mensagem de confirmação da atualização
    """

    id = form.id
    nome = unquote(unquote(form.nome))

    logger.debug(f"Editando o Cliente {nome}")

    try:
        # criando conexão com a base
        session = Session()
        # Consulta para verificar se ja existe a descricao com outro codigo
        cliente = session.query(Cliente).filter(
            Cliente.nome == nome and Cliente.id != id).first()

        if cliente:
            # se foi encontrado retorna o codigo http 400
            error_msg = "Cliente já cadastrado na base"
            logger.warning(
                f"Erro ao editar o cliente '{cliente.nome}', {error_msg}")
            return {"message": error_msg}, 400
        else:

            count = session.query(Cliente).filter(
                Cliente.id == id).update({"nome": nome})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o cliente {nome}")
                return '', 204
            else:
                error_msg = f"O cliente com ID {id} não foi encontrado na base"
                logger.warning(
                    f"Erro ao editar o cliente '{nome}', {error_msg}")
                return '', 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 500


@app.delete('/cliente', tags=[cliente_tag],
            responses={"204": None, "404": None,
                       "409": ErrorSchema, "500": ErrorSchema})
def del_cliente(form: ClenteBuscaDeleteSchema):
    """Exclui um cliente da base de dados com base no codigo id do cliente

    Retorna uma mensagem de exclusão com sucesso.
    """
    id = form.id
    logger.debug(f"Excluindo o Cliente ID #{id}")
    try:
        # criando conexão com a base
        session = Session()

        # fazendo a remoção
        count = session.query(Cliente).filter(Cliente.id == id).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o cliente ID #{id}")
            return '', 204
        else:
            # quando não encontrado retorno o codigo http 404 not found
            error_msg = "Cliente não encontrado na base :/"
            logger.warning(f"Erro ao excluir o cliente #'{id}', {error_msg}")
            return '', 404
    except IntegrityError as e:
        # caso de referencia na tabela agendamento retorna o erro na exclusao
        error_msg = "o cadastro do cliente está\
                     referenciado em um agendamento!"
        logger.warning(f"Erro ao excluir cliente', {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível excluir o cliente :/"
        logger.warning(
            f"Erro ao excluir o cliente com ID #'{id}', {error_msg}")
        print(e)
        return {"message": error_msg}, 500


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClienteSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os clientes cadastrados

    Retorna uma representacao da listagem de clientes
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" % len(clientes))
        # retorna a representação de cliente
        print(clientes)
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um cliente a partir do nome do cliente

    Retorna uma representação do cliente
    """
    cliente_nome = query.nome.strip()
    logger.debug(f"Coletando dados sobre cliente {cliente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(
        Cliente.nome == cliente_nome).first()

    if not cliente:
        # se o cliente não for encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar o cliente '{cliente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cliente encontrado: '{cliente.nome}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200

# ***************************************************  Metodos do Profissional ***************************************
@app.post('/profissional', tags=[profissional_tag],
          responses={"200": ProfissionalViewSchema,
                     "409": ErrorSchema,
                     "400": ErrorSchema})
def add_profissional(form: ProfissionalSchema):
    """Adicionar um profissional à base de dados

    Retorna uma representação do profissional.
    """
    profissional = Profissional(
        nome=form.nome
    )

    logger.debug(
        f"Adicionando um profissional com o nome: '{profissional.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando profissional
        session.add(profissional)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado profissional de nome: '{profissional.nome}'")
        return apresenta_profissional(profissional), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Profissional de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar profissional\
            '{profissional.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar profissional '\
            {profissional.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.put('/profissional', tags=[profissional_tag],
         responses={"204": None, "400": ErrorSchema,
                    "404": None, "500": ErrorSchema})
def put_profissional(form: ProfissionalViewSchema):
    """Editar um profissional já cadastrado na base """
    id = form.id
    nome = unquote(unquote(form.nome))
    logger.debug(f"Editando o Profissional {nome}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta para verificar se ja existe a descricao com outro codigo
        profissional = session.query(Profissional).filter(
            Profissional.nome == nome).filter(Profissional.id != id).first()

        if profissional:
            # se o profissional foi encontrado retorna sem dar o commit
            error_msg = "Profissional já cadastrado na base"
            logger.warning(
                f"Erro ao editar o profissional ID #{id},\
                '{profissional.nome}', {error_msg}")
            return {"message": error_msg}, 400
        else:
            count = session.query(Profissional).filter(
                Profissional.id == id).update({"nome": nome})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o profissional {nome}")
                return '', 204
            else:
                # se não foi encontrado, retorna o codigo not found 404
                error_msg = "O profissional não foi encontrado"
                logger.warning(
                    f"Erro ao editar o profissional '{nome}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar o profissional :/{e.__str__}"
        logger.warning(
            f"Erro ao editar o profissional com ID #'{id}'\
            e profissional {nome}, {error_msg}")
        return {"message": error_msg}, 500


@app.delete('/profissional', tags=[profissional_tag],
            responses={"204": None, "404": None, "500": ErrorSchema})
def del_profissional(form: ProfissionalBuscaExclusaoSchema):
    """Excluiu um profissional cadastrado com base no Id"""
    id = form.id
    logger.debug(f"Excluindo o Profissional ID #{id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Profissional).filter(
            Profissional.id == id).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o profissional ID #{id}")
            return '', 204
        else:
            # se não foi encontrado, retorna o codigo not found 404
            error_msg = "Profissional não encontrado na base :/"
            logger.warning(
                f"Erro ao excluir o profissional #'{id}', {error_msg}")
            return '', 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível excluir o profissional :/{e.__str__}"
        logger.warning(
            f"Erro ao excluir o profissional com ID #'{id}', {error_msg}")
        return {"message": error_msg}, 500


@app.get('/profissionais', tags=[profissional_tag],
         responses={"200": ListagemProfissionalSchema, "404": ErrorSchema})
def get_profissionais():
    """Faz a busca por todos os profissionais cadastrados

    Retorna uma representacao da listagem de profissionais
    """
    logger.debug(f"Coletando profissionais ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    profissionais = session.query(Profissional).all()

    if not profissionais:
        # se não há produtos cadastrados
        return {"profissionais": []}, 200
    else:
        logger.debug(f"%d profissionais encontrados" % len(profissionais))
        # retorna a representação de cliente
        print(profissionais)
        return apresenta_profissionais(profissionais), 200


@app.get('/profissional', tags=[profissional_tag],
         responses={"200": ProfissionalViewSchema, "404": ErrorSchema})
def get_profissional(query: ProfissionalBuscaSchema):
    """Faz a busca por um profissional a partir do nome

    Retorna uma representação do profissional
    """
    profissional_nome = query.nome
    logger.debug(f"Coletando dados sobre profissional {profissional_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    profissional = session.query(Profissional).filter(
        Profissional.nome == profissional_nome).first()

    if not profissional:
        # se o profissional não for encontrado
        error_msg = "Profissional não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar o profissional '{profissional_nome}'\
            , {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Profissional encontrado: '{profissional.nome}'")
        # retorna a representação de profissional
        return apresenta_profissional(profissional), 200


# ***************************************************  Metodos do Serviço ***************************************
@app.post('/servico', tags=[servico_tag],
          responses={"201": None, "400": ErrorSchema})
def post_servico(form: ServicoSchema):
    """Adiciona um novo serviço à base de dados """
    servico = Servico(
        descricao=form.descricao.strip(),
        valor=form.valor
    )
    logger.debug(
        f"Adicionando um servico com a descrição: '{servico.descricao}'\
         e valor = {servico.valor}")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando serviço
        session.add(servico)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado o serviço com a descrição: '{servico.descricao}'\
              e valor = {servico.valor}")
        return apresenta_servico(servico), 201
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Serviço de mesma descrição já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar o serviço '{servico.descricao}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar o serviço '{servico.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.put('/servico', tags=[servico_tag],
         responses={"204": None, "404": None,
                    "409": ErrorSchema, "500": ErrorSchema})
def put_servico(form: ServicoEditSchema):
    """ Editando o serviço com a busca pelo id """
    id = form.id
    descricao = unquote(unquote(form.descricao))
    valor = form.valor

    logger.debug(f"Editando o Serviço {descricao}")
    try:
        # criando conexão com a base
        session = Session()
        # verificar se ja existe a descricao com outro codigo
        servico_busca = session.query(Servico).filter(
            Servico.descricao == descricao).filter(Servico.id != id).first()

        if servico_busca:
            # se o serviço for encontrado retorna sem dar o commit
            error_msg = "Serviço já cadastrado na base"
            logger.warning(
                f"Erro ao editar o serviço '{descricao}', {error_msg}")
            return {"message": error_msg}, 400
        else:
            count = session.query(Servico).filter(Servico.id == id).update(
                {"descricao": descricao, "valor": valor})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o serviço {descricao}")
                return '', 204
            else:
                # se o serviço não foi encontrado, retorna o codigo 404
                error_msg = "O serviço não foi encontrado"
                logger.warning(
                    f"Erro ao editar o serviço '{descricao}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar o serviço :/{e.__str__}"
        logger.warning(f"Erro ao editar o serviço com ID #'{id}', {error_msg}")
        return {"message": error_msg}, 500


@app.get('/servicos', tags=[servico_tag],
         responses={"200": ListagemServicoSchema, "500": ErrorSchema})
def get_servicos():
    """Consultar todos os serviços cadastrados na base de dados

    Retorna uma lista de serviços
    """
    logger.debug(f"Consulta de serviço")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    servicos = session.query(Servico).all()
    try:
        if not servicos:
            # se não há servicos cadastrados
            return {"servicos": []}, 200
        else:
            logger.debug(f"%d servicos encontrados" % len(servicos))
            # retorna a representação de cliente
            print(servicos)
            return apresenta_servicos(servicos), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível consultar os serviços :/{e.__str__}"
        logger.warning(f"Erro ao consultar o serviços , {error_msg}")
        return {"message": error_msg}, 500


@app.get('/servico', tags=[servico_tag],
         responses={"200": ServicoViewSchema, "500": ErrorSchema})
def get_servico(query: ServicoBuscaSchema):
    """Consulta um serviço com base no codigo id

    Retorna a representação de um serviço
    """
    servico_descricao = query.descricao
    logger.debug(f"Consulta de dados sobre serviço {servico_descricao}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    servico = session.query(Servico).filter(
        Servico.descricao == servico_descricao).first()

    if not servico:
        # se o servico não for encontrado
        error_msg = "Serviço não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar o servico '{servico_descricao}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Serviço encontrado: '{servico.descricao}'")
        # retorna a representação de serviço
        return apresenta_servico(servico), 200


@app.delete('/servico', tags=[servico_tag],
            responses={"204": None, "404": ErrorSchema, "500": ErrorSchema})
def del_servico(form: ServicoBuscaDeleteSchema):
    """Excuir o registro de serviço cadastro com base no id"""
    id = form.id

    logger.debug(f"Excluindo o Serviço ID #{id}")
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Servico).filter(Servico.id == id).delete()
        session.commit()

        if count:
            # retorna sem representação com apenas o codigo http 204
            logger.debug(f"Excluindo o serviço ID #{id}")
            return '', 204
        else:
            # se o serviço não foi encontrado, retorna o codigo not found 404
            error_msg = "Serviço não encontrado na base :/"
            logger.warning(f"Erro ao excluir o serviço #'{id}', {error_msg}")
            return '', 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível excluir o serviço :/{e.__str__}"
        logger.warning(
            f"Erro ao excluir o serviço com ID #'{id}', {error_msg}")
        return {"message": error_msg}, 500
