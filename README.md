# Cofre Digital de Prontuários Veterinários

Aplicação desenvolvida em Python com FastAPI para armazenamento e gerenciamento de prontuários veterinários.

Trabalho Prático 1 da disciplina **QXD0099 - Desenvolvimento de Software para Persistência** (UFC - Campus Quixadá).

## Integrantes e o que cada um fez

- **Ithawana de Oliveira Cunha**: Implementação da base: criação da estrutura, models, config, logging e services
- **Mariana Kessia de Lavor Assuncao**: Implementação de F1 a F7, F16 (em service e router) e F17; Correções em alguns arquivos; Arquivo README.
- **Moacir Silva Abreu**: Implementação de F9, F11 a F14; Correções em alguns arquivos;

## Tema

**Prontuários Veterinários**

- **Tipos de arquivos esperados:** PDF, imagens, exames e receitas.
- **Particularidade obrigatória:** metadados de animal, tutor, espécie e data do atendimento.

## Objetivo

O Cofre Digital de Prontuários Veterinários armazena, gerencia e protege documentos digitais de atendimentos clínicos de animais, como prontuários, exames, receitas, laudos e imagens.

Cada documento enviado é guardado no sistema de arquivos e recebe um identificador único e um hash SHA-256. Seus metadados ficam persistidos em JSON e associados ao atendimento (animal, tutor, espécie e data). A partir daí, o documento pode ser consultado, filtrado, baixado, atualizado, excluído e ter sua integridade verificada. O catálogo pode ser exportado em CSV, o cofre pode ser copiado em backups compactados e cada animal possui um histórico clínico com todos os seus documentos. Todas as operações ficam registradas em um arquivo de log, e o comportamento da aplicação é controlado por um arquivo de configuração YAML.

## Requisitos

- Python **3.10 ou superior** (o código usa a sintaxe `str | None`)
- `pip` para instalar as dependências
- Nenhum banco de dados é necessário: toda a persistência é feita em arquivos

## Bibliotecas utilizadas

| Biblioteca | Uso no projeto |
| `fastapi` | Criação da API e das rotas |
| `uvicorn[standard]` | Servidor que executa a aplicação |
| `pydantic` | Modelos e validação dos metadados (`Documento`, `DocumentoCreate`, `DocumentoUpdate`) |
| `pyyaml` | Leitura do arquivo de configuração `config.yaml` |
| `python-multipart` | Recebimento de arquivos via formulário (`multipart/form-data`) no upload |

Módulos da biblioteca padrão do Python:

| Módulo | Uso no projeto |
|---|---|
| `json` | Leitura e escrita dos metadados em `documentos.json` |
| `csv` | Exportação do catálogo de documentos |
| `hashlib` | Cálculo do hash SHA-256 |
| `mimetypes` | Identificação do tipo MIME pela extensão |
| `logging` | Sistema de logs |
| `zipfile` | Compactação dos backups |
| `pathlib` | Manipulação de caminhos de arquivos e diretórios |

## Instalação

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone https://github.com/ithawana/cofre-prontuarios-veterinarios.git
   cd cofre-prontuarios-veterinarios
   ```

2. Crie e ative um ambiente virtual:

   ```powershell
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   ```bash
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Execução

Na pasta do projeto (onde está o `main.py`), inicie o servidor:

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger), em que é possível testar todos os endpoints, fica em:

- `http://127.0.0.1:8000/docs`

### Dados de demonstração

O repositório já inclui documentos cadastrados em `storage/`. Para recriar o conjunto de 15 documentos fictícios de demonstração, mantenha a API rodando e execute, em outro terminal na raiz do projeto:

```bash
python dados_teste/popular.py    # cadastra os documentos via POST /documentos/
python dados_teste/verificar.py  # confere listagem, filtros, downloads, integridade e estatísticas
```

Mais detalhes sobre esses dados estão em `dados_teste/LEIA_ME.md`.

## Configuração (`config.yaml`)

```yaml
storage:
  arquivos: "storage/files"
  metadata: "storage/metadata"
  backups: "storage/backups"
  exports: "storage/exports"
  logs: "storage/logs"

persistencia:
  arquivo_metadata: "documentos.json"

backup:
  nome_prefixo: "backup"

logging:
  nivel: "INFO"
  arquivo: "sistema.log"
```

| Chave | Efeito |
|---|---|
| `storage.*` | Diretórios onde a aplicação grava arquivos, metadados, backups, exportações e logs (relativos à pasta do projeto) |
| `persistencia.arquivo_metadata` | Nome do arquivo JSON de metadados |
| `backup.nome_prefixo` | Prefixo do nome dos arquivos de backup |
| `logging.nivel` | Nível mínimo registrado no log (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `logging.arquivo` | Nome do arquivo de log |

As configurações são lidas na inicialização. Após alterar o arquivo, é preciso reiniciar o servidor.

## Estrutura do projeto

```
cofre-prontuarios-veterinarios/
|--- main.py                    # Cria a aplicação FastAPI e registra as rotas
|--- config.yaml                # Arquivo externo de configuração (YAML)
|--- config.py                  # Lê o config.yaml e expõe as configurações
|--- logging_config.py          # Configura o logging a partir do config.yaml
|--- requirements.txt           # Dependências do projeto
|--- models/
│   |--- documento.py           # Modelos Pydantic e enums (Categoria, Especie)
|--- routes/
│   |--- documentos.py          # Upload, listagem/filtros, consulta, download, atualização,
│   │                          # exclusão e histórico do animal (F16)
│   |--- integridade.py         # Verificação de integridade (SHA-256)
│   |--- relatorios.py          # Estatísticas do cofre e exportação CSV
│   |--- backup.py              # Geração de backup compactado
|--- services/
│   |--- documento_service.py   # Leitura/escrita do JSON, estatísticas e histórico do animal
│   |--- arquivo_service.py     # Armazenamento físico, SHA-256, extensão e tipo MIME
│   |--- backup_service.py      # Geração de backups compactados (.zip)
|--- storage/
│   |--- files/                 # Arquivos originais armazenados (nomeados pelo ID)
│   |--- metadata/
│   │   |--- documentos.json    # Persistência principal dos metadados
│   |--- logs/                  # Arquivo de log da aplicação (sistema.log)
│   |--- exports/               # Catálogo exportado em CSV
│   |--- backups/               # Backups gerados (.zip)
|--- dados_teste/               # Documentos fictícios e scripts de carga/verificação
```

Responsabilidades:
- **models**: define o formato dos dados e valida as entradas.
- **routes**: recebe requisições HTTP e retorna as respostas com o status_code adequado.
- **services**: concentra a lógica de persistência (arquivos físicos, JSON, CSV e backups).

## Metadados específicos do domínio

Cada documento é representado pela classe Pydantic `Documento` (`models/documento.py`). Além dos metadados gerais exigidos (`id`, `nome_original`, `nome_armazenado`, `extensao`, `tipo_mime`, `tamanho`, `categoria`, `descricao`, `data_upload` e `sha256`), o modelo possui os seguintes metadados do domínio veterinário:

| Campo | Tipo | Descrição |
|---|---|---|
| `animal` | texto | Nome do animal atendido |
| `tutor` | texto | Nome do tutor (responsável) do animal |
| `especie` | enum | `cachorro`, `gato`, `ave` ou `outro` |
| `data_atendimento` | data | Data do atendimento veterinário (`AAAA-MM-DD`) |

A `categoria` também foi adaptada ao tema e aceita os valores `prontuario`, `exame`, `receita` e `imagem`.

Onde os metadados do domínio são utilizados:

- **Upload e atualização:** são informados no `POST` e podem ser alterados no `PUT`.
- **Filtros (F7):** `categoria`, `animal` e `especie`.
- **Estatísticas (F8):** quantidade de documentos por espécie.
- **Exportação CSV (F13):** todos aparecem como colunas.
- **Histórico clínico (F16):** `animal` e `tutor` identificam o paciente; `data_atendimento` define a ordem.

## Principais endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/documentos/` | Criação/Upload de um arquivo com seus metadados (F1) |
| `GET` | `/documentos/` | Lista todos os documentos, com filtros opcionais (F2, F7) |
| `GET` | `/documentos/{id}` | Consulta os metadados de um documento (F3) |
| `GET` | `/documentos/{id}/download` | Baixa o arquivo original (F4) |
| `PUT` | `/documentos/{id}` | Atualiza os metadados de um documento (F5) |
| `DELETE` | `/documentos/{id}` | Exclui o documento (F6) |
| `GET` | `/documentos/estatisticas` | Estatísticas calculadas a partir dos dados persistidos (F8) |
| `GET` | `/documentos/{id}/integridade` | Recalcula o SHA-256 e compara com o hash original (F9) |
| `GET` | `/exportar/csv` | Exporta o catálogo de documentos em CSV (F13) |
| `POST` | `/backup` | Gera um backup compactado (.zip) do cofre (F14) |
| `GET` | `/documentos/{animal}/historico` | Histórico clínico do animal (F16) |


### Comportamento da exclusão (F6)
Ao receber `DELETE /documentos/{id}`, o sistema:

1. verifica se o documento existe nos metadados. Caso não exista, retorna **404**;
2. remove o arquivo físico correspondente de `storage/files/`. Se o arquivo já não existir no disco, a situação é registrada no log como `WARNING` e a exclusão continua;
3. remove o registro do documento de `documentos.json`;
4. registra a operação no log.

A exclusão é definitiva. Para preservar um documento antes de excluí-lo, é necessário gerar um backup.

### Códigos HTTP utilizados

| Código | Situação |
|---|---|
| `200` | Operação realizada com sucesso |
| `201` | Documento criado no upload |
| `404` | Documento inexistente, arquivo físico não encontrado ou animal sem documentos |
| `422` | Dados inválidos (campo obrigatório ausente, categoria/espécie inválida, data em formato inválido) |
| `500` | Erro interno (JSON de metadados corrompido, falha de leitura ou escrita) |

## Funcionalidade específica do tema (F16): Histórico clínico do animal

```
GET /documentos/{animal}
```

Reúne todos os documentos de um animal (prontuários, exames, receitas e imagens) **em ordem cronológica de atendimento**, do mais antigo para o mais recente, formando a linha do tempo clínica do paciente.

**Como funciona:**
1. Lê os documentos persistidos em `documentos.json`.
2. Seleciona os documentos cujo `animal` corresponde ao nome informado (sem diferenciar maiúsculas de minúsculas).
3. Se o `tutor` for informado, mantém apenas os documentos daquele tutor. Isso diferencia animais com o mesmo nome que pertencem a tutores diferentes.
4. Ordena os documentos pelo campo `data_atendimento`.
5. Retorna o nome do animal, o total de documentos e a lista ordenada.

**Metadados do domínio utilizados:** `animal`, `tutor` e `data_atendimento`.

**Diferença em relação ao filtro (F7):** o filtro apenas seleciona os documentos. O histórico ordena os documentos pela data do atendimento e também permite identificar o animal pelo tutor.

**Respostas:**

- **200**: histórico encontrado.
- **404**: nenhum documento encontrado para o animal (ou para o animal e o tutor informados).
- **500**: erro ao ler os metadados.

A consulta é registrada no log (`HISTORICO animal=Kiwi total=2`).


## Logging

O sistema usa o módulo `logging` do Python e grava os eventos em `storage/logs/sistema.log` (caminho e nível definidos no `config.yaml`).

Formato: `data hora NÍVEL OPERAÇÃO informações`

```
2026-10-08 18:12:12 INFO SISTEMA_INICIADO
2026-10-08 18:12:13 INFO UPLOAD id=12 arquivo=10_laudo_kiwi.pdf
2026-10-08 18:15:40 INFO DOWNLOAD id=12 arquivo=10_laudo_kiwi.pdf
2026-10-08 18:20:02 INFO INTEGRIDADE_OK id=12
2026-10-08 18:21:30 WARNING INTEGRIDADE_FALHOU id=3
2026-10-08 18:22:11 INFO HISTORICO animal=Kiwi total=2
```

- **INFO**: operações realizadas com sucesso.
- **WARNING**: situações anormais que não são falhas do sistema (documento inexistente, integridade comprometida).
- **ERROR**: falhas de leitura ou escrita e erros inesperados.
