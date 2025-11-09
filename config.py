import os


class Settings:
    # Configuration de l'application
    PROJECT_NAME: str = "Outils en Ligne - Base64"
    PROJECT_VERSION: str = "1.0.0"

    # Configuration serveur (sécurisée)
    HOST: str = os.getenv("HOST", "127.0.0.1")  # Localhost par défaut
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"

    # Configuration SEO
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    META_DESCRIPTION: str = "Collection d'outils en ligne gratuits pour développeurs"
    META_KEYWORDS: list[str] = [
        "base64",
        "encodeur base64",
        "décodeur base64",
        "outils en ligne",
        "encodeur en ligne",
        "décodeur en ligne",
        "utf-8",
        "ascii",
    ]

    # Configuration sécurité
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    @property
    def server_config(self) -> dict:
        return {"host": self.HOST, "port": self.PORT, "reload": self.RELOAD}


settings = Settings()
