from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from enum import Enum

# categorias que um documento pode ter
class Categoria(str, Enum):
    PRONTUARIO = "prontuario"
    EXAME = "exame"
    RECEITA = "receita"
    IMAGEM = "imagem"

# espécies de animais atendidos
class Especie(str, Enum):
    CACHORRO = "cachorro"
    GATO = "gato"
    AVE = "ave"
    OUTRO = "outro"


# dados que o usuário envia no upload (POST /documentos)
class DocumentoCreate(BaseModel):
    categoria: Categoria
    descricao: str | None = None
    animal: str
    tutor: str
    especie: Especie
    data_atendimento: date

class DocumentoUpdate(BaseModel):
    categoria: Categoria | None = None
    descricao: str | None = None
    animal: str | None = None
    tutor: str | None = None
    especie: Especie | None = None
    data_atendimento: date | None = None

# documento completo, já salvo no sistema    
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
