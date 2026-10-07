from fastapi import FastAPI

from routes.documentos import router as documentos_router


app = FastAPI(
    title="Cofre Digital de Prontuários Veterinários",
    description="API para armazenamento e gerenciamento de prontuários veterinários.",
    version="1.0.0"
)

app.include_router(documentos_router)