import yaml
from pathlib import Path

# Carrega as configurações do arquivo YAML externo

CAMINHO_CONFIG = Path(__file__).parent / "config.yaml"


with open(CAMINHO_CONFIG, "r", encoding="utf-8") as arquivo:
    CONFIG = yaml.safe_load(arquivo)


DIRETORIO_ARQUIVOS = Path(CONFIG["storage"]["arquivos"])
DIRETORIO_METADATA = Path(CONFIG["storage"]["metadata"])
CAMINHO_METADATA_JSON = DIRETORIO_METADATA / CONFIG["persistencia"]["arquivo_metadata"]
DIRETORIO_BACKUPS = Path(CONFIG["storage"]["backups"])
DIRETORIO_EXPORTS = Path(CONFIG["storage"]["exports"])
DIRETORIO_LOGS = Path(CONFIG["storage"]["logs"])

PREFIXO_BACKUP = CONFIG["backup"]["nome_prefixo"]