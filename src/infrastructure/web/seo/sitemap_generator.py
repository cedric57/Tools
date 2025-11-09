import os
from datetime import datetime

from fastapi.templating import Jinja2Templates


class SitemapGenerator:
    @staticmethod
    def generate_sitemap(base_url: str) -> str:
        """
        Génère un sitemap XML sécurisé en utilisant des templates Jinja2
        """
        base_url = base_url.rstrip("/")

        # Configuration des templates
        templates_path = os.path.join(os.path.dirname(__file__), "../../presentation/templates")
        templates = Jinja2Templates(directory=templates_path)

        # Données pour le sitemap
        urls = [
            {"loc": "/", "priority": "1.0", "changefreq": "daily", "lastmod": datetime.now().strftime("%Y-%m-%d")},
            {
                "loc": "/encode",
                "priority": "0.8",
                "changefreq": "monthly",
                "lastmod": datetime.now().strftime("%Y-%m-%d"),
            },
            {
                "loc": "/decode",
                "priority": "0.8",
                "changefreq": "monthly",
                "lastmod": datetime.now().strftime("%Y-%m-%d"),
            },
        ]

        # Rendre le template
        context = {"base_url": base_url, "urls": urls}

        template = templates.get_template("sitemap.xml.j2")
        return template.render(context)
