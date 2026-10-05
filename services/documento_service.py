import json
from pathlib import Path

from config import CAMINHO_METADATA

CAMINHO_JSON = CAMINHO_METADATA

def ler_documentos() -> list[dict]:
    """Lê os documentos armazenados no arquivo JSON."""

    if not CAMINHO_JSON.exists():
        return []

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_documentos(documentos: list[dict]) -> None:
    """Salva os documentos no arquivo JSON."""

    CAMINHO_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(
            documentos,
            f,
            indent=4,
            ensure_ascii=False,
            default=str
        )


def buscar_por_id(documento_id: int) -> dict | None:
    """Busca um documento pelo seu ID."""

    documentos = ler_documentos()

    for documento in documentos:
        if documento["id"] == documento_id:
            return documento

    return None


def adicionar(documento: dict) -> None:
    """Adiciona um novo documento ao arquivo JSON."""

    documentos = ler_documentos()

    documentos.append(documento)

    salvar_documentos(documentos)


def atualizar(documento_id: int, novo_documento: dict) -> bool:
    """Atualiza um documento existente."""

    documentos = ler_documentos()

    for indice, documento in enumerate(documentos):

        if documento["id"] == documento_id:

            novo_documento["id"] = documento_id

            documentos[indice] = novo_documento

            salvar_documentos(documentos)

            return True

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
        return False

    salvar_documentos(nova_lista)

    return True