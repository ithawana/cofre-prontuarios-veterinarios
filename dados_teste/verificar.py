"""Verifica os documentos de demonstracao, sem alterar os dados da API."""
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = Path(__file__).resolve().parent
URL = "http://127.0.0.1:8000"


def acessar(caminho, binario=False):
    with urlopen(URL + caminho, timeout=15) as resposta:
        conteudo = resposta.read()
        return conteudo if binario else json.loads(conteudo)


def verificar(condicao, descricao):
    print(("OK" if condicao else "FALHOU") + " - " + descricao)
    return bool(condicao)


def main():
    with (BASE / "manifesto.json").open(encoding="utf-8") as arquivo:
        exemplos = json.load(arquivo)
    try:
        todos = acessar("/documentos/")
        mapa = {(d["nome_original"], d["animal"]): d for d in todos}
        presentes = [mapa.get((e["arquivo"], e["animal"])) for e in exemplos]
        testes = []
        testes.append(verificar(len(todos) >= 15, "Pelo menos 15 documentos cadastrados (F2)"))
        testes.append(verificar(all(presentes), "Os 15 documentos ficticios estao na listagem (F1/F2)"))
        testes.append(verificar(len({d["extensao"] for d in todos}) >= 4,
                                 "Pelo menos 4 extensoes (requisito de apresentacao)"))
        testes.append(verificar(len({d["categoria"] for d in todos}) >= 3,
                                 "Pelo menos 3 categorias (requisito de apresentacao)"))
        if not all(presentes):
            print("Cadastre os documentos ausentes com: python dados_teste/popular.py")
            return 1

        testes.append(verificar(all(
            acessar(f"/documentos/{doc['id']}")["animal"] == exemplo["animal"]
            for doc, exemplo in zip(presentes, exemplos)
        ), "Consulta por identificador dos 15 documentos (F3)"))
        testes.append(verificar(all(
            hashlib.sha256(acessar(f"/documentos/{doc['id']}/download", binario=True)).hexdigest()
            == exemplo["sha256_esperado"]
            for doc, exemplo in zip(presentes, exemplos)
        ), "Downloads iguais aos arquivos originais (F4)"))
        testes.append(verificar(all(
            acessar(f"/documentos/{doc['id']}/integridade")["integro"] is True
            for doc in presentes
        ), "Integridade SHA-256 dos 15 documentos (F9)"))

        for campo, valor in (("categoria", "exame"), ("animal", "Rex"), ("especie", "gato")):
            filtrados = acessar("/documentos/?" + urlencode({campo: valor}))
            testes.append(verificar(
                bool(filtrados) and all(d[campo].lower() == valor.lower() for d in filtrados),
                f"Filtro {campo}={valor} (F7)",
            ))

        estat = acessar("/documentos/estatisticas")
        testes.append(verificar(
            estat["total_documentos"] == len(todos) and
            estat["tamanho_total_bytes"] == sum(d["tamanho"] for d in todos) and
            sum(estat["quantidade_por_categoria"].values()) == len(todos) and
            sum(estat["quantidade_por_extensao"].values()) == len(todos) and
            sum(estat["quantidade_por_especie"].values()) == len(todos),
            "Estatisticas baseadas nos dados persistidos (F8)",
        ))
        try:
            acessar(f"/documentos/{max(d['id'] for d in todos) + 1000}")
            nao_encontrado = False
        except HTTPError as erro:
            nao_encontrado = erro.code == 404
        testes.append(verificar(nao_encontrado, "Documento inexistente retorna HTTP 404 (F3/F17)"))
        print(f"\nResultado: {sum(testes)}/{len(testes)} verificacoes passaram.")
        return 0 if all(testes) else 1
    except (HTTPError, URLError, OSError, ValueError, KeyError) as erro:
        print("ERRO: verifique se a API esta ligada e se os dados foram carregados.")
        print(erro)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
