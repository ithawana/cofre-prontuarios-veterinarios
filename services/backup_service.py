from pathlib import Path
from datetime import datetime
import zipfile

from config import (
    DIRETORIO_ARQUIVOS,
    DIRETORIO_METADATA,
    DIRETORIO_BACKUPS,
    PREFIXO_BACKUP,
)
from logging_config import logger


def criar_backup() -> Path:
    """Cria um arquivo ZIP contendo os arquivos e metadados do cofre."""

    DIRETORIO_BACKUPS.mkdir(parents=True, exist_ok=True)

    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nome_backup = f"{PREFIXO_BACKUP}_{data_hora}.zip"

    caminho_backup = DIRETORIO_BACKUPS / nome_backup

    with zipfile.ZipFile(
        caminho_backup,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        if DIRETORIO_ARQUIVOS.exists():
            for arquivo in DIRETORIO_ARQUIVOS.rglob("*"):
                if arquivo.is_file():
                    zip_file.write(
                        arquivo,
                        arquivo.relative_to(DIRETORIO_ARQUIVOS.parent)
                    )

        if DIRETORIO_METADATA.exists():
            for arquivo in DIRETORIO_METADATA.rglob("*"):
                if arquivo.is_file():
                    zip_file.write(
                        arquivo,
                        arquivo.relative_to(DIRETORIO_METADATA.parent)
                    )

    logger.info("Backup criado: %s", nome_backup)

    return caminho_backup