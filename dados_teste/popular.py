"""Cadastra os 15 documentos ficticios utilizando POST /documentos/."""
import json
import mimetypes
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent
URL = "http://127.0.0.1:8000"


def consultar_documentos():
    with urlopen(URL + "/documentos/", timeout=10) as resposta:
        return json.load(resposta)


def enviar_documento(dados):
    limite = "----CofreTesteFicticio"
    partes = []
    for campo in ("categoria", "descricao", "animal", "tutor", "especie", "data_atendimento"):
        partes.append(
            f"--{limite}\r\nContent-Disposition: form-data; name=\"{campo}\"\r\n\r\n"
            f"{dados[campo]}\r\n".encode("utf-8")
        )
    arquivo = BASE / "arquivos" / dados["arquivo"]
    tipo = mimetypes.guess_type(arquivo.name)[0] or "application/octet-stream"
    partes.append(
        f"--{limite}\r\nContent-Disposition: form-data; name=\"arquivo\"; "
        f"filename=\"{arquivo.name}\"\r\nContent-Type: {tipo}\r\n\r\n".encode("utf-8")
    )
    partes.append(arquivo.read_bytes())
    partes.append(f"\r\n--{limite}--\r\n".encode("utf-8"))
    requisicao = Request(
        URL + "/documentos/", data=b"".join(partes), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={limite}"},
    )
    with urlopen(requisicao, timeout=20) as resposta:
        return json.load(resposta)


def main():
    if not (RAIZ / "main.py").exists():
        print("ERRO: extraia a pasta dados_teste dentro da raiz do projeto (ao lado de main.py).")
        return 1

    with (BASE / "manifesto.json").open(encoding="utf-8") as arquivo:
        exemplos = json.load(arquivo)
    try:
        existentes = consultar_documentos()
    except (HTTPError, URLError, ValueError) as erro:
        print("ERRO: nao foi possivel consultar a API. Inicie o Uvicorn e confira o JSON.")
        print(erro)
        return 1

    # Protege contra arquivos antigos sem registro no JSON, problema visto neste projeto.
    pasta_arquivos = RAIZ / "storage" / "files"
    fisicos = {p.name for p in pasta_arquivos.iterdir() if p.is_file() and p.name != ".gitkeep"} if pasta_arquivos.exists() else set()
    registrados = {d["nome_armazenado"] for d in existentes}
    orfaos = sorted(fisicos - registrados)
    if orfaos:
        print("PARADO POR SEGURANCA: existem arquivos fisicos sem metadados:")
        print(", ".join(orfaos))
        print("Faca backup e resolva essa inconsistencia antes de executar o carregamento.")
        return 1

    cadastrados = {(d["nome_original"], d["animal"]) for d in existentes}
    feitos = 0
    for dados in exemplos:
        identificacao = (dados["arquivo"], dados["animal"])
        if identificacao in cadastrados:
            print("JA EXISTE:", dados["arquivo"])
            continue
        try:
            resultado = enviar_documento(dados)
        except HTTPError as erro:
            print("FALHA no upload de", dados["arquivo"], "HTTP", erro.code)
            print(erro.read().decode("utf-8", errors="replace")[:500])
            return 1
        except (URLError, ValueError, OSError) as erro:
            print("FALHA no upload de", dados["arquivo"], ":", erro)
            return 1
        print(f"CADASTRADO: ID {resultado['id']} - {dados['arquivo']}")
        feitos += 1
        cadastrados.add(identificacao)

    print(f"Concluido: {feitos} novos documentos. Total atual: {len(consultar_documentos())}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
