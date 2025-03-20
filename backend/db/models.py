from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.session import Base

class Utilizador(Base):
    __tablename__ = "Utilizador"

    UtilizadorID = Column(Integer, primary_key=True, index=True)
    NomeUtilizador = Column(String)
    DataNasc = Column(Date)
    Contacto = Column(Integer)
    Email = Column(String, index=True)
    PasswordHash = Column(String)
    Salt = Column(String)
    Foto = Column(String)
    TUID = Column(Integer, ForeignKey("TipoUtilizador.TUID"))

    TipoUtilizador = relationship("TipoUtilizador", back_populates="Utilizadores")

class TipoUtilizador(Base):
    __tablename__ = "TipoUtilizador"
    
    TUID = Column(Integer, primary_key=True, index=True)
    DescTU = Column(String)

    Utilizadores = relationship("Utilizador", back_populates="TipoUtilizador")

