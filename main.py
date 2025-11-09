import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import settings
from src.infrastructure.web.controllers.base64_controller import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Outil en ligne gratuit pour encoder et décoder le Base64",
    version=settings.PROJECT_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=settings.DEBUG,
)

# Montage des routes
app.include_router(router)

# Montage des fichiers statiques
static_path = os.path.join(os.path.dirname(__file__), "src/presentation/static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "base64-tool"}


def main():
    """Point d'entrée principal de l'application"""
    import uvicorn

    server_config = settings.server_config

    print("🚀 Démarrage de l'application...")
    print(f"📍 URL: http://{server_config['host']}:{server_config['port']}")
    print(f"📚 Documentation: http://{server_config['host']}:{server_config['port']}/api/docs")
    print(f"🔄 Rechargement automatique: {'Activé' if server_config['reload'] else 'Désactivé'}")

    uvicorn.run("main:app", host=server_config["host"], port=server_config["port"], reload=server_config["reload"])


if __name__ == "__main__":
    main()
