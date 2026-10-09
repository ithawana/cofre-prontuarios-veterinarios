from fastapi import APIRouter, HTTPException

from services import backup_service
from logging_config import logger

router = APIRouter(tags=["backup"])

# F14: Backup compactado
@router.post("/backup")
def gerar_backup():
    try:
        caminho = backup_service.criar_backup()
        tamanho = caminho.stat().st_size

    except (OSError, RuntimeError):
        logger.exception("ERRO_CRIACAO_BACKUP")
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar backup"
        )

    return {
        "mensagem": "Backup criado com sucesso",
        "arquivo": caminho.name,
        "tamanho": tamanho
    }