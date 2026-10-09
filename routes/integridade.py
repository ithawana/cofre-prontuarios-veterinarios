from fastapi import APIRouter, HTTPException

from services import documento_service, arquivo_service
from logging_config import logger

router = APIRouter(tags=["integridade"])


# F9: Verificação de integridade individual
@router.get("/documentos/{documento_id}/integridade")
def verificar_integridade(documento_id: int):
    try:
        documento = documento_service.buscar_por_id(documento_id)
    except Exception:
        logger.exception("ERRO_INTEGRIDADE id=%d", documento_id)
        raise HTTPException(status_code=500, detail="Erro ao ler os documentos")

    if documento is None:
        logger.warning("INTEGRIDADE_DOCUMENTO_NAO_ENCONTRADO id=%d", documento_id)
        raise HTTPException(
            status_code=404,
            detail="Documento não encontrado"
        )

    caminho = arquivo_service.localizar_arquivo(
        documento["nome_armazenado"]
    )

    if not caminho.is_file():
        logger.warning("INTEGRIDADE_ARQUIVO_NAO_ENCONTRADO id=%d", documento_id)
        raise HTTPException(
            status_code=404,
            detail="Arquivo físico não encontrado"
        )

    try:
        hash_atual = arquivo_service.calcular_sha256(caminho)
    except OSError:
        logger.exception("INTEGRIDADE_ERRO_LEITURA id=%d", documento_id)
        raise HTTPException(
            status_code=500,
            detail="Erro ao ler arquivo armazenado"
        )

    hash_original = documento["sha256"]
    integro = hash_atual == hash_original

    if integro:
        logger.info("INTEGRIDADE_OK id=%d", documento_id)
    else:
        logger.warning("INTEGRIDADE_FALHOU id=%d", documento_id)

    return {
        "id": documento_id,
        "nome": documento["nome_original"],
        "hash_original": hash_original,
        "hash_atual": hash_atual,
        "integro": integro
    }