import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import LOGGING_CONFIG, settings
from src.presentation.api.v1.endpoints import analytics, contact, tools

# Configuration du logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    logger.info(f"🚀 Démarrage de {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"📊 Environnement: {settings.ENVIRONMENT}")
    logger.info(f"🐛 Debug: {settings.DEBUG}")

    yield

    # Shutdown
    logger.info("👋 Arrêt de l'application")


# Application FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API backend performante pour la suite d'outils en ligne",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(tools.router, prefix=settings.API_V1_STR + "/tools", tags=["tools"])

app.include_router(analytics.router, prefix=settings.API_V1_STR + "/analytics", tags=["analytics"])

app.include_router(contact.router, prefix=settings.API_V1_STR + "/contact", tags=["contact"])


# Health check étendu
@app.get("/health")
async def health_check():
    """Health check complet de l'application"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }


# Endpoint racine
@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": f"Bienvenue sur {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs",
        "health": "/health",
        "openapi": "/api/openapi.json",
    }


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erreur non gérée: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Une erreur interne est survenue",
            "error": str(exc) if settings.DEBUG else "Internal server error",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG,
        log_config=LOGGING_CONFIG,
    )
