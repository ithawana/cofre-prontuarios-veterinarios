from fastapi import FastAPI

from routes.documentos import router as documentos_router

from routes.relatorios import router as relatorios_router

from routes.integridade import router as integridade_router


app = FastAPI(
    title="Cofre Digital de Prontuários Veterinários",
    description="API para armazenamento e gerenciamento de prontuários veterinários.",
    version="1.0.0"
)

app.include_router(relatorios_router)
app.include_router(documentos_router)
app.include_router(integridade_router)