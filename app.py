from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session, Autor, Editora, Livro
from logger import logger
from schemas import *
from flask_cors import CORS
from urllib.parse import unquote

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Documentação: Swagger, Redoc ou RapiDoc")
autor_tag = Tag(name="Autor", description="Adição e visualização de autores")
editora_tag = Tag(name="Editora", description="Adição e visualização de editoras")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi"""
    return redirect('/openapi')

### GERENCIAR AUTOR ###
@app.post('/autor', tags=[autor_tag],
          responses={"200": AutorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_autor(form: AutorSchema):
    """
        Adiciona um novo Autor.
        Retorna uma representação de Autor.
    """
    autor = Autor(nome=form.nome)
    logger.debug(f"Adicionando autor de nome: '{autor.nome}'")

    try:
        # Criando conexão com a base de dados
        session = Session()
        # Adicionando um Autor
        session.add(autor)
        # Efetivando a adição do novo Autor na tabela
        session.commit()

        logger.debug(f"Autor '{autor.nome}' adicionado com sucesso.")
        return apresenta_autor(autor), 200
    except IntegrityError as e:
        # IntegrityError para evitar duplicidade do nome
        error_msg = "Já existe um autor com o mesmo nome."

        logger.warning(f"Erro ao adicionar autor '{autor.nome}': {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        # Erro imprevisto
        error_msg = "Não foi possível salvar o novo autor."
        
        logger.warning(f"Erro ao adicionar autor '{autor.nome}': {error_msg}")
        return {"message": error_msg}, 400

@app.get('/autores', tags=[autor_tag],
          responses={"200": ListagemAutoresSchema, "404": ErrorSchema})
def get_autores():
    """
        Busca por todos os autores cadastrados.
        Retorna uma lista de autores.
    """
    logger.debug("Coletando todos os autores.")

    # Criando conexão com a base de dados
    session = Session()
    # Realizando a busca
    autores = session.query(Autor).all()

    if not autores:
        return {"autores": []}, 200
    else:
        logger.debug(f"{len(autores)} autores encontrados.")
        return apresenta_autores(autores), 200

### GERENCIAR EDITORA ###
@app.post('/editora', tags=[editora_tag],
          responses={"200": EditoraViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_editora(form: EditoraSchema):
    """
        Adiciona uma nova Editora.
        Retorna uma representação da Editora.
    """
    editora = Editora(nome=form.nome)
    logger.debug(f"Adicionando editora de nome: '{editora.nome}'")
    
    try:
        # Criando conexão com a base de dados
        session = Session()
        # Adicionando uma Editora
        session.add(editora)
        # Efetivando a adição da nova Editora na tabela
        session.commit()

        logger.debug(f"Editora '{editora.nome}' adicionada com sucesso.")
        return apresenta_editora(editora), 200
    except IntegrityError as e:
        # IntegrityError para evitar duplicidade do nome
        error_msg = "Já existe uma editora com o mesmo nome."

        logger.warning(f"Erro ao adicionar editora '{editora.nome}': {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        # Erro imprevisto
        error_msg = "Não foi possível salvar a editora."

        logger.warning(f"Erro ao adicionar editora '{editora.nome}': {error_msg}")
        return {"message": error_msg}, 400

@app.get('/editoras', tags=[editora_tag],
          responses={"200": ListagemEditorasSchema, "404": ErrorSchema})
def get_editoras():
    """
        Busca por todas as editoras cadastradas.
        Retorna uma lista de editoras.
    """
    logger.debug("Coletando todas as editoras.")

    # Criando conexão com a base de dados
    session = Session()
    # Realizando a busca
    editoras = session.query(Editora).all()

    if not editoras:
        return {"editoras": []}, 200
    else:
        logger.debug(f"{len(editoras)} editoras encontradas.")
        return apresenta_editoras(editoras), 200

### GERENCIAR LIVRO ###

@app.post('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    """
        Adiciona um novo livro.
    """
    logger.debug(f"Adicionando livro de título: '{form.titulo}'")

    try:
        session = Session()

        # Buscar a editora pelo ID
        editora = session.query(Editora).filter_by(id=form.id_editora).first()
        if not editora:
            error_msg = "Editora não encontrada."

            logger.warning(f"Erro ao adicionar livro '{form.titulo}': {error_msg}")
            return {"message": error_msg}, 400

        # Buscar os autores pelo ID
        autores = session.query(Autor).filter(Autor.id.in_(form.ids_autores)).all()
        if not autores or len(autores) != len(form.ids_autores):
            error_msg = "Um ou mais autores não encontrados."
            logger.warning(f"Erro ao adicionar livro '{form.titulo}': {error_msg}")
            return {"message": error_msg}, 400

        # Criar o livro e associar autores
        livro = Livro(
            titulo=form.titulo,
            ano_publicacao=form.ano_publicacao,
            editora=editora,
            autores=autores
        )

        # Adicionar e salvar no banco
        session.add(livro)
        session.commit()
        
        logger.debug(f"Livro '{livro.titulo}' adicionado com sucesso.")
        return apresenta_livro(livro), 200

    except IntegrityError:
        # IntegrityError para evitar duplicidade do nome
        error_msg = "Já existe um livro com o mesmo título."

        logger.warning(f"Erro ao adicionar livro '{form.titulo}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Erro imprevisto
        session.rollback()
        error_msg = "Não foi possível salvar o livro."

        logger.error(f"Erro ao adicionar livro '{form.titulo}': {str(e)}")
        return {"message": error_msg}, 400

    finally:
        session.close()

@app.get('/livros', tags=[livro_tag],
          responses={"200": ListagemLivrosSchema, "404": ErrorSchema})
def get_livros():
    """
        Busca por todos os livros cadastrados.
        Retorna uma lista de livros.
    """
    logger.debug("Coletando todos os livros.")

    # Criando conexão com a base de dados
    session = Session()
    # Realizando a busca
    livros = session.query(Livro).all()

    if not livros:
        return {"livros": []}, 200
    else:
        logger.debug(f"{len(livros)} livros encontrados.")
        return apresenta_livros(livros), 200

@app.get('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "404": ErrorSchema})
def get_livro(query: LivroBuscaSchema):
    """
        Busca por um livro a partir do título.
        Retorna os dados do livro encontrado.
    """
    livro_titulo = query.titulo
    logger.debug(f"Coletando dados do livro de título: {livro_titulo}")
    
    # Criando conexão com a base de dados
    session = Session()
    # Realizando a busca
    livro = session.query(Livro).filter(Livro.titulo == livro_titulo).first()

    if not livro:
        # Se o livro não for encontrado
        error_msg = "Livro não encontrado."
        logger.warning(f"Erro ao buscar livro '{livro_titulo}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Livro encontrado: '{livro.titulo}'")
        return apresenta_livro(livro), 200

@app.delete('/livro', tags=[livro_tag],
            responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query: LivroBuscaSchema):
    """
        Deleta um Livro a partir do nome do livro informado.
        Retorna uma mensagem de confirmação da remoção.
    """
    # Descodifica o título do livro da URL (caso tenha sido codificado)
    livro_titulo = unquote(unquote(query.titulo))
    print(livro_titulo)
    
    # Log para rastrear a operação de exclusão
    logger.debug(f"Deletando dados sobre Livro #{livro_titulo}")

    # Cria a sessão para interação com a base de dados
    session = Session()

    try:
        # Busca o livro a ser deletado na base de dados, considerando o título
        livro = session.query(Livro).filter(Livro.titulo == livro_titulo).first()

        if not livro:
            # Caso o livro não seja encontrado na base de dados, retorna erro 404
            error_msg = "Livro não encontrado na base de dados."

            logger.warning(f"Erro ao deletar Livro de título: '#{livro_titulo}', {error_msg}")
            return {"message": error_msg}, 404

        # Desassocia os autores do livro antes de deletá-lo
        livro.autores.clear()  # Remove todas as relações Many-to-Many com autores

        # Deleta o livro da base de dados
        session.delete(livro)
        session.commit()  # Confirma as alterações na base

        # Se o livro foi deletado com sucesso, retorna mensagem de confirmação
        logger.debug(f"Deletado Livro de título: #{livro_titulo} e suas associações")
        return {"message": "Livro removido", "título": livro_titulo}

    except Exception as e:
        # Erro imprevisto
        session.rollback()  # Reverte qualquer alteração feita na base até o momento do erro
        error_msg = f"Erro ao tentar excluir o Livro de título: '#{livro_titulo}': {str(e)}"
        
        # Log do erro para diagnóstico
        logger.error(error_msg)
        return {"message": error_msg}, 500

    finally:
        # Fecha a sessão para liberar os recursos da conexão com a base de dados
        session.close()
