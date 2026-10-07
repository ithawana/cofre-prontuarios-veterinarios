import logging
from config import DIRETORIO_LOGS, NIVEL_LOG, NOME_ARQUIVO_LOG

DIRETORIO_LOGS.mkdir(parents=True, exist_ok=True)

CAMINHO_LOG = DIRETORIO_LOGS / NOME_ARQUIVO_LOG

logging.basicConfig(
    level=getattr(logging, NIVEL_LOG),
    filename=CAMINHO_LOG,
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("cofre_digital")