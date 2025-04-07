from sqlalchemy.ext.declarative import declarative_base

# Criação da classe Base, que será a classe base para todas as classes de modelo no SQLAlchemy
# Essa classe permite que o SQLAlchemy mapeie os modelos de dados para as tabelas do banco de dados
# Todas as classes de modelo que você definir devem herdar de 'Base'
Base = declarative_base()
