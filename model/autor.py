from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from model import Base

# Tabela de associação para o relacionamento Many-to-Many entre as entidades 'Livro' e 'Autor'
# A tabela 'livro_autor' armazena as associações entre livros e autores.
# Cada entrada na tabela representa um autor que está associado a um livro.
# As chaves estrangeiras (ForeignKey) apontam para as tabelas 'livro' e 'autor', garantindo a integridade referencial.
livro_autor = Table(
    "livro_autor",  # Nome da tabela de associação
    Base.metadata,  # Referência ao metadata da base
    Column("id_livro", Integer, ForeignKey("livro.pk_livro"), primary_key=True),  # Chave estrangeira para o livro
    Column("id_autor", Integer, ForeignKey("autor.pk_autor"), primary_key=True)  # Chave estrangeira para o autor
)

class Autor(Base):
    __tablename__ = 'autor'  # Nome da tabela no banco de dados

    id = Column("pk_autor", Integer, primary_key=True)  # Identificador único para o autor
    nome = Column(String(200), unique=True, nullable=False)  # Nome do autor (único e não nulo)

    # Relacionamento Many-to-Many com Livro
    livros = relationship("Livro", secondary=livro_autor, back_populates="autores")

    def __init__(self, nome: str):
        self.nome = nome
