from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum


class Categoria(str, Enum):
    PRONTUARIO = "prontuario"
    EXAME = "exame"
    RECEITA = "receita"
    IMAGEM = "imagem"


class Especie(str, Enum):
    CACHORRO = "cachorro"
    GATO = "gato"
    AVE = "ave"
    OUTRO = "outro"


class Documento(BaseModel):
    # Metadados gerais do cofre
    id: int
    nome_original: str
    nome_armazenado: str
    extensao: str
    tipo_mime: str | None = None
    tamanho: int
    categoria: Categoria
    descricao: str | None = None
    data_upload: datetime
    sha256: str

    # Metadados específicos do tema 
    animal: str
    tutor: str
    especie: Especie
    data_atendimento: date

class DocumentoCreate(BaseModel):
    categoria: Categoria
    descricao: str | None = None
    animal: str
    tutor: str
    especie: Especie
    data_atendimento: date