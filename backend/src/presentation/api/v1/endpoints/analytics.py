from fastapi import APIRouter

router = APIRouter()


@router.get("/usage")
async def get_usage_analytics():
    """Retourne les analytics d'utilisation"""
    from src.application.use_cases.base64_operations import Base64UseCases
    from src.infrastructure.repositories.base64_repository_impl import Base64RepositoryImpl

    repository = Base64RepositoryImpl()
    use_cases = Base64UseCases(repository)

    analytics = await use_cases.get_analytics()
    return analytics


@router.get("/popular-encodings")
async def get_popular_encodings():
    """Retourne les encodages les plus utilisés"""
    from src.application.use_cases.base64_operations import Base64UseCases
    from src.infrastructure.repositories.base64_repository_impl import Base64RepositoryImpl

    repository = Base64RepositoryImpl()
    use_cases = Base64UseCases(repository)

    analytics = await use_cases.get_analytics()
    return {"popular_encodings": analytics["encoding_usage"]}
