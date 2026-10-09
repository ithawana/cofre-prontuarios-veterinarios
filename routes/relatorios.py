import csv

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from services import documento_service
from config import DIRETORIO_EXPORTS
from logging_config import logger

router = APIRouter(tags=["relatorios"])

# F8: Estatísticas do Cofre Digital
@router.get("/documentos/estatisticas")
def estatisticas_documentos():
    try:
        return documento_service.calcular_estatisticas()
    except Exception:
        logger.exception("ERRO_ESTATISTICAS")
        raise HTTPException(status_code=500, detail="Erro ao calcular as estatísticas")

# F13: Exportação do catálogo para CSV
@router.get("/exportar/csv")
def exportar_csv():
    try:
        documentos = documento_service.ler_documentos()
    except Exception:
        logger.exception("ERRO_EXPORTACAO_CSV")
        raise HTTPException(status_code=500, detail="Erro ao ler os documentos")

    DIRETORIO_EXPORTS.mkdir(parents=True, exist_ok=True)
    caminho_csv = DIRETORIO_EXPORTS / "catalogo_documentos.csv"

    colunas = [
        "id", "nome_original", "nome_armazenado", "extensao",
        "tipo_mime", "tamanho", "categoria", "descricao",
        "data_upload", "sha256", "animal", "tutor",
        "especie", "data_atendimento"
    ]

    try:
        with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()

            for documento in documentos:
                escritor.writerow({
                    campo: documento.get(campo, "")
                    for campo in colunas
                })

    except OSError:
        logger.exception("ERRO_EXPORTACAO_CSV")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar arquivo CSV"
        )

    logger.info("EXPORTACAO_CSV total=%d", len(documentos))

    return FileResponse(
        path=caminho_csv,
        media_type="text/csv",
        filename="catalogo_documentos.csv"
    )
