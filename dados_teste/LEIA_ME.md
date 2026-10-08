# Dados fictícios de demonstração - Cofre Digital Veterinário

Conjunto de **15 documentos fictícios**, destinado exclusivamente a testes do trabalho de Persistência. Nenhum nome de tutor representa uma pessoa real. Os PDFs e PNGs são ilustrativos e não têm validade clínica.

**Requisitos atendidos pelo conjunto:** 15 documentos, 5 extensões (`.txt`, `.csv`, `.pdf`, `.png`, `.json`), 4 categorias (`prontuario`, `exame`, `receita`, `imagem`), arquivos de texto e binários, metadados veterinários (animal, tutor, espécie, data de atendimento). O `manifesto.json` possui os campos para o upload e o SHA-256 esperado de cada arquivo.

## Instalação dos dados na aplicação

1. Descompacte a pasta `dados_teste` **na raiz do projeto**, ao lado de `main.py`.
2. Preserve uma cópia da pasta `storage` antes do carregamento. Confira que `storage/files` não possui arquivos sem registro no JSON; o script interrompe o processo se detectar essa situação.
3. Inicie a API em um terminal dentro da raiz do projeto:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --reload
   ```

4. Abra **outro terminal**, também na raiz, e execute:

   ```powershell
   .\.venv\Scripts\python.exe dados_teste\popular.py
   ```

   O script realiza 15 requisições HTTP `POST /documentos/`, respeitando o modelo Pydantic. Se executar novamente, ele ignora os documentos já cadastrados com o mesmo nome e animal.

5. Confira o resultado sem modificar nenhum documento:

   ```powershell
   .\.venv\Scripts\python.exe dados_teste\verificar.py
   ```

6. Acesse `http://127.0.0.1:8000/docs` para ver os endpoints e conferir manualmente a listagem, filtros, estatísticas e integridade.

## Teste da persistência

Após o carregamento, interrompa o Uvicorn (`Ctrl+C`) e inicie-o de novo. Execute `GET /documentos/` e `GET /documentos/estatisticas`. Devem continuar disponíveis os documentos e suas contagens. Confira também `storage/metadata/documentos.json` e `storage/files`.

Para confirmar que uma consulta não reescreve o JSON, anote a saída deste comando antes e depois da listagem:

```powershell
Get-FileHash .\storage\metadata\documentos.json -Algorithm SHA256
```

Os hashes devem ser iguais. Evite editar `documentos.json` manualmente. Não execute testes de exclusão nos 15 documentos que serão utilizados na apresentação.

## Commit no GitHub

Se quiser incluir os dados de demonstração no GitHub, será necessário permitir que os arquivos em `storage/files` e `storage/metadata/documentos.json` sejam versionados (ajustando o `.gitignore`). Faça o commit somente **depois** de conferir a consistência entre os arquivos físicos e o JSON. Nunca inclua dados reais de pacientes ou tutores.

Alternativamente, mantenha a pasta `dados_teste` no repositório: qualquer pessoa poderá recriar os 15 cadastros executando o script de carregamento.

## Testes de atualização e exclusão sem prejudicar a apresentação

Na subpasta `descartaveis/` existem dois arquivos de texto extras, **que não são cadastrados pelo script**. Eles servem para testar manualmente no Swagger:

- `teste_atualizacao.txt`: realize `POST /documentos/` com metadados fictícios válidos, anote o ID; execute `PUT /documentos/{id}` com `{"descricao":"Descricao alterada no teste"}`; confirme no `GET /documentos/{id}` e no JSON.
- `teste_exclusao.txt`: realize `POST /documentos/`, anote o ID; execute `DELETE /documentos/{id}`; confira que o registro saiu do JSON e que o arquivo físico foi removido.

Exemplo de dados de cadastro para ambos: categoria `prontuario`, animal `Teste`, tutor `Tutor Ficticio`, especie `cachorro`, data_atendimento `2026-09-16`.

**Não exclua os 15 arquivos principais da demonstração**. Ao final, ficam 15 documentos válidos na API.
