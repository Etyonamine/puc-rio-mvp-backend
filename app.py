from datetime import datetime
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Agendamento, Cliente, Profissional, Servico
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


@app.post('/agendamento', tags=[agendamento_tag],
          responses={"201": AgendamentoViewSchema,
                     "404": ErrorSchema,
                     "500": ErrorSchema})
def add_agendamento(form: AgendamentoSchema):
    """Adicionar o Agendamento de serviços do cliente

       Retorna uma representação do Agendamento do cliente.
    """
    agendamento = Agendamento(
        data_agenda=datetime.strptime(form.data_agenda, "%d/%m/%Y %H:%M:%S"),
        observacao=form.observacao,
        cliente_id=form.cliente_id,
        profissional_id=form.profissional_id,
        servico_id=form.servico_id
    )
    logger.debug(
        f"Adicionando agendamento de serviço de cliente na\
         data de: '{agendamento.data_agenda}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando agendamento
        session.add(agendamento)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado agendamento do cliente com\
             data em: '{agendamento.data_agenda}'")
        return apresenta_agendamento(agendamento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Agendamento com a mesma data já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar  o agendamento do cliente com data = '\
            {agendamento.data_agenda}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente, {error_msg}")
        return {"message": error_msg}, 400


@app.put('/agendamento', tags=[agendamento_tag],
         responses={"204": None,
                    "404": ErrorSchema,
                    "500": ErrorSchema})
def upd_agendamento(form: AgendamentoEditSchema):
    """Editar uma agenda já cadastrado na base """
    id = form.id
    data_agenda = datetime.strptime(form.data_agenda, "%Y-%m-%d %H:%M:%S")
    logger.debug(f"Editando o agendamento #{id}")
    try:

        # criando conexão com a base
        session = Session()
        # Consulta se ja existe a descricao com outro codigo
        agendamento = session.query(Agendamento)\
                             .filter(Agendamento.profissional_id
                                     == form.profissional_id)\
                             .filter(Agendamento.data_agenda == data_agenda)\
                             .filter(Agendamento.id != id)\
                             .filter(
                                    Agendamento.cliente_id != form.cliente_id)\
                             .first()

        if agendamento:
            # se foi encontrado retorna sem dar o commit
            error_msg = "Existe outro agendamento com\
                         o mesmo profissional para outro cliente!"
            logger.warning(
                f"Erro ao editar o profissional ID #{id}, {error_msg}")
            return {"message": error_msg}, 400
        else:
            logger.warning(f"observacao = {form.observacao}")
            count = session.query(Agendamento)\
                           .filter(Agendamento.id == id)\
                           .update({"cliente_id": form.cliente_id,
                                    "profissional_id": form.profissional_id,
                                    "servico_id": form.servico_id,
                                    "observacao": form.observacao})
            session.commit()
            if count:
                # retorna sem representação com apenas o codigo http 204
                logger.debug(f"Editado o agendamento ID #{id}")
                return '', 204
            else:
                # se não foi encontrado, retorna o codigo not found 404
                error_msg = "O agendamento não foi encontrado"
                logger.warning(
                    f"Erro ao editar o agendamento ID #'{id}', {error_msg}")
                return '', 404
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível editar o agendamento :/{e.__str__}"
        logger.warning(
            f"Erro ao editar o agendamento com ID #'{id}', {error_msg}")
        return {"message": error_msg}, 500


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
