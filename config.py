import yaml
from pathlib import Path

# Diretório principal do projeto
BASE_DIR = Path(__file__).resolve().parent

# Arquivo de configuração
CAMINHO_CONFIG = BASE_DIR / "config.yaml"

with open(CAMINHO_CONFIG, "r", encoding="utf-8") as arquivo:
    CONFIG = yaml.safe_load(arquivo)

# Diretórios configurados no YAML
DIRETORIO_ARQUIVOS = BASE_DIR / CONFIG["storage"]["arquivos"]
DIRETORIO_METADATA = BASE_DIR / CONFIG["storage"]["metadata"]
DIRETORIO_BACKUPS = BASE_DIR / CONFIG["storage"]["backups"]
DIRETORIO_EXPORTS = BASE_DIR / CONFIG["storage"]["exports"]
DIRETORIO_LOGS = BASE_DIR / CONFIG["storage"]["logs"]

# Arquivo de metadados
ARQUIVO_METADATA = DIRETORIO_METADATA / CONFIG["persistencia"]["arquivo_metadata"]

# Configuração dos backups
PREFIXO_BACKUP = CONFIG["backup"]["nome_prefixo"]

# Configuração dos logs
NIVEL_LOG = CONFIG["logging"]["nivel"]
NOME_ARQUIVO_LOG = CONFIG["logging"]["arquivo"]