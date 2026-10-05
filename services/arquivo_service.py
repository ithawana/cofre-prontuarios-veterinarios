from pathlib import Path
import hashlib
import mimetypes

from config import DIRETORIO_ARQUIVOS


def salvar_arquivo(arquivo, nome_armazenado: str) -> Path:
    """Salva o arquivo enviado na pasta storage/files"""
    caminho = DIRETORIO_ARQUIVOS / nome_armazenado

    with open(caminho, "wb") as file:
        file.write(arquivo.file.read())

    return caminho


def calcular_sha256(caminho: Path) -> str:
    """Calcula o SHA-256 do arquivo para verificar sua integridade"""
    sha256 = hashlib.sha256()

    with open(caminho, "rb") as file:
        while bloco := file.read(4096):
            sha256.update(bloco)

    return sha256.hexdigest()


def obter_extensao(nome_original: str) -> str:
    """Obtém a extensão do arquivo original"""
    return Path(nome_original).suffix.lower()


def obter_tipo_mime(nome_original: str) -> str | None:
    """Identifica o tipo MIME do arquivo a partir do seu nome"""
    tipo_mime, _ = mimetypes.guess_type(nome_original)
    return tipo_mime


def localizar_arquivo(nome_armazenado: str) -> Path:
    """Retorna o caminho do arquivo armazenado"""
    return DIRETORIO_ARQUIVOS / nome_armazenado


def deletar_arquivo(nome_armazenado: str) -> None:
    """Exclui o arquivo físico do armazenamento"""
    caminho = localizar_arquivo(nome_armazenado)

    if caminho.exists():
        caminho.unlink()