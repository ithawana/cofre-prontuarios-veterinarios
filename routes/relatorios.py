from fastapi import APIRouter
from services import documento_service

router = APIRouter(tags=["relatorios"])


# F8: Estatísticas do Cofre Digital
@router.get("/documentos/estatisticas")
def estatisticas_documentos():
    return documento_service.calcular_estatisticas()