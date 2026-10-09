# Cofre Digital de Prontuários Veterinários

Aplicação desenvolvida em Python com FastAPI para armazenamento e gerenciamento de prontuários veterinários.

Trabalho Prático 1 da disciplina **QXD0099 - Desenvolvimento de Software para Persistência** (UFC - Campus Quixadá).

## Integrantes

- Ithawana de Oliveira Cunha
- Mariana Kessia de Lavor Assuncao
- Moacir Silva Abreu

## Tema

**Prontuários Veterinários**

- **Tipos de arquivos esperados:** PDF, imagens, exames e receitas.
- **Particularidade obrigatória:** metadados de animal, tutor, espécie e data do atendimento.

## Objetivo

O Cofre Digital de Prontuários Veterinários armazena, gerencia e protege documentos digitais de atendimentos clínicos de animais, como prontuários, exames, receitas, laudos e imagens.

Cada documento enviado é guardado no sistema de arquivos e recebe um identificador único e um hash SHA-256. Seus metadados ficam persistidos em JSON e associados ao atendimento (animal, tutor, espécie e data). A partir daí, o documento pode ser consultado, filtrado, baixado, atualizado, excluído e ter sua integridade verificada. Todas as operações ficam registradas em um arquivo de log, e o comportamento da aplicação é controlado por um arquivo de configuração YAML.

## Requisitos

- Python **3.10 ou superior** (o código usa a sintaxe `str | None`)
- `pip` para instalar as dependências
- Nenhum banco de dados é necessário: toda a persistência é feita em arquivos


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

Inicie o servidor **a partir da raiz do projeto**, a pasta onde está o `main.py`. Os caminhos definidos no `config.yaml` são relativos a essa pasta.

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

## Estrutura do projeto

```
cofre-prontuarios-veterinarios/
|--- main.py                    
    # Cria a aplicação FastAPI e registra as rotas
|--- config.yaml                
    # Arquivo externo de configuração (YAML)
|--- config.py                  
    # Lê o config.yaml e expõe as configurações
|--- logging_config.py          
    # Configura o logging a partir do config.yaml
|--- requirements.txt           
    # Dependências do projeto
|--- models/
│   |--- documento.py           
        # Modelos Pydantic e enums (Categoria, Especie)
|--- routes/
│   |--- documentos.py          
        # Upload, listagem/filtros, consulta, download, atualização, exclusão
│   |--- integridade.py         
        # Verificação de integridade (SHA-256)
│   |--- relatorios.py          
        # Estatísticas do cofre
|--- services/
│   |--- documento_service.py   
        # Leitura/escrita do JSON de metadados e estatísticas
│   |--- arquivo_service.py     
        # Armazenamento físico, SHA-256, extensão e tipo MIME
│   |--- backup_service.py      
        # Geração de backups compactados (.zip)
|--- storage/
│   |--- files/                 
        # Arquivos originais armazenados (nomeados pelo ID)
│   |--- metadata/
│   │   |--- documentos.json    
            # Persistência principal dos metadados
│   |--- logs/                  
        # Arquivo de log da aplicação (sistema.log)
│   |--- exports/               
        # Arquivos exportados
│   |--- backups/               
        # Backups gerados
|--- dados_teste/               
        # Documentos fictícios e scripts de carga/verificação
```

Responsabilidades:
- **models**: define o formato dos dados e valida as entradas.
- **routes**: recebe requisições HTTP e retorna o status_code.
- **services**: concentra a lógica de persistência.


## Principais endpoints

| Método | Rota | Descrição |
| `POST` | `/documentos/` | Upload de um arquivo com seus metadados (F1) |
| `GET` | `/documentos/` | Lista todos os documentos, com filtros opcionais (F2, F7) |
| `GET` | `/documentos/{id}` | Consulta os metadados de um documento (F3) |
| `GET` | `/documentos/{id}/download` | Baixa o arquivo original (F4) |
| `PUT` | `/documentos/{id}` | Atualiza os metadados de um documento (F5) |
| `DELETE` | `/documentos/{id}` | Exclui o documento e seu arquivo físico (F6) |
| `GET` | `/documentos/estatisticas` | Estatísticas calculadas a partir dos dados persistidos (F8) |
| `GET` | `/documentos/{id}/integridade` | Recalcula o SHA-256 e compara com o hash original (F9) |

### Filtros disponíveis em `GET/documentos/`
| Parâmetro | Tipo de atributo | Exemplo |
| `categoria` | geral | `/documentos/?categoria=exame` |
| `animal` | específico do domínio | `/documentos/?animal=Rex` |
| `especie` | específico do domínio | `/documentos/?especie=gato` |
