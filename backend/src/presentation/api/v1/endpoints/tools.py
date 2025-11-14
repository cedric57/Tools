from fastapi import APIRouter

from application.dto.base64_dto import EncodingCategoriesResponse, ToolConfig
from application.use_cases.base64_operations import Base64UseCases
from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response
from infrastructure.repositories.base64_repository_impl import Base64RepositoryImpl

router = APIRouter()

# Initialisation des use cases
repository = Base64RepositoryImpl()
base64_use_cases = Base64UseCases(repository)


@router.post("/encode", response_model=Base64Response)
async def encode_base64(request: Base64EncodeRequest):
    """Encode un texte en Base64"""
    return await base64_use_cases.encode_text(request)


@router.post("/decode", response_model=Base64Response)
async def decode_base64(request: Base64DecodeRequest):
    """Décode un texte Base64"""
    return await base64_use_cases.decode_text(request)


@router.get("/encodings", response_model=EncodingCategoriesResponse)
async def get_encoding_categories():
    """Retourne la liste des encodages supportés"""
    return EncodingCategoriesResponse.from_domain()


@router.get("/config", response_model=ToolConfig)
async def get_tool_config():
    """Retourne la configuration de l'outil"""
    return ToolConfig(
        name="Base64 Tools",
        version="1.0.0",
        supported_encodings=["utf-8", "ascii", "latin-1", "windows-1252", "utf-16"],
    )


@router.get("/health")
async def tools_health():
    """Health check spécifique aux outils"""
    return {
        "status": "healthy",
        "service": "base64-tools",
        "features": ["encode", "decode", "multiple_encodings", "line_by_line"],
    }
