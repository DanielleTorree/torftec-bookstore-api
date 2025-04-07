from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from model import Base

class Editora(Base):
    __tablename__ = 'editora'  # Nome da tabela no banco de dados

    # Definição da chave primária 'id' para a tabela 'editora'
    id = Column("pk_editora", Integer, primary_key=True)

    # Definição da coluna 'nome', com limite de 100 caracteres e valor único
    # Não pode ser nula
    nome = Column(String(100), unique=True, nullable=False)

    # Relacionamento One-to-Many com a tabela 'Livro'
    # Um 'Editora' pode ter muitos 'Livros' associados a ela
    # 'back_populates' define o nome do campo correspondente na tabela 'Livro'
    livros = relationship("Livro", back_populates="editora")

    def __init__(self, nome: str):
        """
        Construtor da classe Editora. Inicializa uma nova editora com o nome fornecido.

        :param nome: O nome da editora (obrigatório).
        """
        self.nome = nome
