from pathlib import Path
import hashlib
import mimetypes

from config import DIRETORIO_ARQUIVOS
from logging_config import logger


def salvar_arquivo(arquivo, nome_armazenado: str) -> Path:
    """Salva o arquivo enviado na pasta storage/files"""

    caminho = DIRETORIO_ARQUIVOS / nome_armazenado

    with open(caminho, "wb") as file:
        file.write(arquivo.file.read())

    logger.info("Arquivo salvo: %s", nome_armazenado)

    return caminho


def calcular_sha256(caminho: Path) -> str:
    """Calcula o SHA-256 do arquivo para verificar sua integridade"""

    sha256 = hashlib.sha256()

    with open(caminho, "rb") as file:
        while bloco := file.read(4096):
            sha256.update(bloco)

    resultado = sha256.hexdigest()

    logger.info("SHA-256 calculado para o arquivo: %s", caminho.name)

    return resultado


def obter_extensao(nome_original: str) -> str:
    """Obtém a extensão do arquivo original"""

    extensao = Path(nome_original).suffix.lower()

    logger.debug(
        "Extensão identificada: %s -> %s",
        nome_original,
        extensao
    )

    return extensao


def obter_tipo_mime(nome_original: str) -> str | None:
    """Identifica o tipo MIME do arquivo a partir do seu nome"""

    tipo_mime, _ = mimetypes.guess_type(nome_original)

    logger.debug(
        "Tipo MIME identificado: %s -> %s",
        nome_original,
        tipo_mime
    )

    return tipo_mime


def localizar_arquivo(nome_armazenado: str) -> Path:
    """Retorna o caminho do arquivo armazenado"""

    caminho = DIRETORIO_ARQUIVOS / nome_armazenado

    return caminho


def deletar_arquivo(nome_armazenado: str) -> None:
    """Exclui o arquivo físico do armazenamento"""

    caminho = localizar_arquivo(nome_armazenado)

    if caminho.exists():
        caminho.unlink()
        logger.info("Arquivo excluído: %s", nome_armazenado)
    else:
        logger.warning(
            "Tentativa de excluir arquivo inexistente: %s",
            nome_armazenado
        )