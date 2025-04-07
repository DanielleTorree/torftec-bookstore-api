from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base
from model.autor import livro_autor  # Associações entre livros e autores
from model.editora import Editora  # Importa o modelo da editora

class Livro(Base):
    __tablename__ = 'livro'  # Nome da tabela no banco de dados

    # Definição da chave primária 'id' para a tabela 'livro'
    id = Column("pk_livro", Integer, primary_key=True)

    # Definição da coluna 'titulo', com limite de 200 caracteres e valor único
    titulo = Column(String(200), unique=True, nullable=False)

    # Definição da coluna 'ano_publicacao', com data e hora de publicação do livro
    # Caso não seja fornecida, é atribuído o valor da data/hora atual
    ano_publicacao = Column(DateTime, default=datetime.now)

    # Relacionamento Many-to-Many com a tabela 'Autor' via tabela associativa 'livro_autor'
    # 'back_populates' define o nome do campo correspondente na tabela 'Autor'
    autores = relationship("Autor", secondary=livro_autor, back_populates="livros")

    # Relacionamento Many-to-One com a tabela 'Editora', usando a chave estrangeira 'id_editora'
    # 'back_populates' define o nome do campo correspondente na tabela 'Editora'
    id_editora = Column(Integer, ForeignKey("editora.pk_editora"))
    editora = relationship("Editora", back_populates="livros")

    def __init__(self, titulo: str, ano_publicacao: Union[DateTime, None] = None, editora: Editora = None, autores=None):
        """
        Construtor da classe Livro. Inicializa um novo livro com as informações fornecidas.

        :param titulo: O título do livro (obrigatório).
        :param ano_publicacao: A data de publicação do livro (opcional, se não fornecido, usa a data/hora atual).
        :param editora: A editora do livro (opcional).
        :param autores: Lista de autores associados ao livro (opcional, padrão é uma lista vazia).
        """
        self.titulo = titulo
        self.ano_publicacao = ano_publicacao if ano_publicacao else datetime.now()  # Usa a data atual se não for fornecida
        self.editora = editora
        self.autores = autores if autores is not None else []  # Define uma lista vazia se 'autores' não for fornecido
