import json
from pathlib import Path

from config import ARQUIVO_METADATA
from logging_config import logger

CAMINHO_JSON = ARQUIVO_METADATA


def ler_documentos() -> list[dict]:
    """Lê os documentos armazenados no arquivo JSON."""

    if not CAMINHO_JSON.exists():
        logger.warning("Arquivo de metadados não encontrado: %s", CAMINHO_JSON)
        return []

    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            documentos = json.load(f)

    except (OSError, json.JSONDecodeError):
        logger.exception("ERRO_LEITURA_JSON")
        raise

    logger.info("Metadados dos documentos carregados.")

    return documentos

def salvar_documentos(documentos: list[dict]) -> None:
    """Salva os documentos no arquivo JSON."""

    CAMINHO_JSON.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
            json.dump(
                documentos,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )

    except (OSError, TypeError, ValueError):
        logger.exception("ERRO_ESCRITA_JSON")
        raise

    logger.info(
        "Metadados dos documentos salvos. Total de registros: %d",
        len(documentos)
    )


def buscar_por_id(documento_id: int) -> dict | None:
    """Busca um documento pelo seu ID."""

    documentos = ler_documentos()

    for documento in documentos:
        if documento["id"] == documento_id:
            logger.info("Documento encontrado: ID %d", documento_id)
            return documento

    logger.warning("Documento não encontrado: ID %d", documento_id)

    return None


def adicionar(documento: dict) -> None:
    """Adiciona um novo documento ao arquivo JSON."""

    documentos = ler_documentos()

    documentos.append(documento)

    salvar_documentos(documentos)

    logger.info("Documento adicionado: ID %d", documento["id"])


def atualizar(documento_id: int, novo_documento: dict) -> bool:
    """Atualiza um documento existente."""

    documentos = ler_documentos()

    for indice, documento in enumerate(documentos):

        if documento["id"] == documento_id:

            novo_documento["id"] = documento_id

            documentos[indice] = novo_documento

            salvar_documentos(documentos)

            logger.info("Documento atualizado: ID %d", documento_id)

            return True

    logger.warning(
        "Não foi possível atualizar. Documento não encontrado: ID %d",
        documento_id
    )

    return False


def remover(documento_id: int) -> bool:
    """Remove um documento pelo ID."""

    documentos = ler_documentos()

    nova_lista = [
        documento
        for documento in documentos
        if documento["id"] != documento_id
    ]

    if len(nova_lista) == len(documentos):
        logger.warning(
            "Não foi possível remover. Documento não encontrado: ID %d",
            documento_id
        )
        return False

    salvar_documentos(nova_lista)

    logger.info("Documento removido: ID %d", documento_id)

    return True

# F8: Estatísticas do Cofre Digital
def calcular_estatisticas() -> dict:
    documentos = ler_documentos()

    por_extensao = {}
    por_categoria = {}
    por_especie = {}

    for documento in documentos:
        extensao = documento["extensao"]
        categoria = documento["categoria"]
        especie = documento["especie"]

        por_extensao[extensao] = por_extensao.get(extensao, 0) + 1
        por_categoria[categoria] = por_categoria.get(categoria, 0) + 1
        por_especie[especie] = por_especie.get(especie, 0) + 1

    return {
        "total_documentos": len(documentos),
        "tamanho_total_bytes": sum(doc["tamanho"] for doc in documentos),
        "quantidade_por_extensao": por_extensao,
        "quantidade_por_categoria": por_categoria,
        "quantidade_por_especie": por_especie
    }