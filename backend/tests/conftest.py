import os
import sys

import pytest
from fastapi.testclient import TestClient

# Configuration du PYTHONPATH
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(backend_dir, "src")
sys.path.insert(0, src_dir)

# Import de l'application FastAPI
try:
    from main import app

    print("✅ Application FastAPI importée avec succès")
    print("Routes disponibles:", [route.path for route in app.routes])
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    raise


@pytest.fixture
def client():
    """Fixture pour le client de test FastAPI"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def base64_repository():
    from application.repositories.base64_repository import Base64Repository

    return Base64Repository()


@pytest.fixture
def base64_operations(base64_repository):
    from application.use_cases.base64_operations import Base64Operations

    return Base64Operations(base64_repository)
