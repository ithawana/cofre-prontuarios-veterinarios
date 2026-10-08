from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Response

from datetime import datetime, date

from models.documento import Documento, DocumentoCreate, DocumentoUpdate
from services import documento_service, arquivo_service

from logging_config import logger


router = APIRouter(
    prefix="/documentos",
    tags=["documentos"]
)


# F1: Upload e armazenamento de arquivos    
@router.post("/", response_model=Documento)
def upload_documento(
    categoria: str = Form(...),
    descricao: str | None = Form(None),
    animal: str = Form(...),
    tutor: str = Form(...),
    especie: str = Form(...),
    data_atendimento: date = Form(...),
    arquivo: UploadFile = File(...)
):
    try:
        dados = DocumentoCreate(
            categoria=categoria,
            descricao=descricao,
            animal=animal,
            tutor=tutor,
            especie=especie,
            data_atendimento=data_atendimento
        )

        documentos = documento_service.ler_documentos()

        novo_id = max(
            [doc["id"] for doc in documentos], 
            default=0
        ) + 1

        extensao = arquivo_service.obter_extensao(arquivo.filename)
        tipo_mime = arquivo_service.obter_tipo_mime(arquivo.filename)

        nome_arquivo = f"{novo_id}{extensao}"

        caminho_arquivo = arquivo_service.salvar_arquivo(
            arquivo,
            nome_arquivo
        )

        sha256 = arquivo_service.calcular_sha256(caminho_arquivo)

        documento = Documento(
            id=novo_id,
            nome_original=arquivo.filename,
            nome_armazenado=nome_arquivo,
            extensao=extensao,
            tipo_mime=tipo_mime,
            tamanho=caminho_arquivo.stat().st_size,
            # .stat() retorna informações sobre o arquivo, como tamanho, data de modificação etc. 
            # .stat().st_size retorna o tamanho do arquivo em bytes.
            categoria=categoria,
            descricao=descricao,
            data_upload=datetime.now(),
            sha256=sha256,
            animal=animal,
            tutor=tutor,
            especie=especie,
            data_atendimento=data_atendimento
        )

        documento_service.adicionar(
            documento.model_dump(mode="json") # transforma em dict
        )

        logger.info(
            "UPLOAD id=%d arquivo=%s",
            novo_id,
            arquivo.filename
        )

        return documento

    except Exception as erro:
        logger.exception("ERRO_UPLOAD arquivo=%s", arquivo.filename)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload do documento: {erro}"
        )

# F2 e F7: Listagem e filtragem de documentos
@router.get("/", response_model=list[Documento])
def listar_documentos(
    categoria: str | None = None,
    animal: str | None = None,
    especie: str | None = None
):
    documentos = documento_service.ler_documentos()

    if categoria:
        documentos = [
            documento for documento in documentos
            if documento["categoria"].lower() == categoria.lower()
        ]

    if animal:
        documentos = [
            documento for documento in documentos
            if documento["animal"].lower() == animal.lower()
        ]

    if especie:
        documentos = [
            documento for documento in documentos
            if documento["especie"].lower() == especie.lower()
        ]

    logger.info(
        "CONSULTA_LISTAGEM total=%d",
        len(documentos)
    )

    return documentos

# F3: Consulta de documentos por ID
@router.get("/{documento_id}", response_model=Documento)
def buscar_documento(documento_id: int):
    documento = documento_service.buscar_por_id(documento_id)

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento não encontrado"
        )

    return documento


# F4: Download de arquivo
@router.get("/{documento_id}/download")
def baixar_documento(documento_id: int):
    documento = documento_service.buscar_por_id(documento_id)

    if documento is None:
        raise HTTPException(
            status_code=404,
            detail="Documento não encontrado"
        )

    caminho = arquivo_service.localizar_arquivo(
        documento["nome_armazenado"]
    )

    with open(caminho, "rb") as arquivo:
        conteudo = arquivo.read()

    logger.info(
        "DOWNLOAD id=%d arquivo=%s",
        documento_id,
        documento["nome_original"]
    )

    return Response( # devolve o conteúdo do arquivo pela API
        content=conteudo,
        media_type=documento["tipo_mime"]
    )


# F5: Atualização de metadados do documento
@router.put("/{documento_id}", response_model=Documento)
def atualizar_documento(
    documento_id: int,
    dados: DocumentoUpdate
):
    documento = documento_service.buscar_por_id(documento_id)

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento não encontrado"
        )

    dados_atualizados = dados.model_dump(
        exclude_unset=True # ignora campos não enviados
    )

    documento.update(dados_atualizados)

    documento_service.atualizar(
        documento_id,
        documento
    )

    return documento


# F6: Exclusão de documento
@router.delete("/{documento_id}")
def excluir_documento(documento_id: int):

    documento = documento_service.buscar_por_id(documento_id)

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento não encontrado"
        )

    arquivo_service.deletar_arquivo(
        documento["nome_armazenado"]
    )

    documento_service.remover(documento_id)

    return {"message": "Documento excluído com sucesso"}

# F8: Consulta de documentos por tutor 