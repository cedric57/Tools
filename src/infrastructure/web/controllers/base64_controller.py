import os

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from backend.src.application.dto import PageContext, SEOConfig
from backend.src.application.use_cases import Base64UseCases
from backend.src.domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest
from backend.src.infrastructure.repositories.base64_repository_impl import (
    Base64RepositoryImpl,
)
from ....infrastructure.web.seo.meta_generator import MetaGenerator
from ....infrastructure.web.seo.sitemap_generator import SitemapGenerator

router = APIRouter()

# Configuration des templates
templates_path = os.path.join(
    os.path.dirname(__file__), "../../../presentation/templates"
)
templates = Jinja2Templates(directory=templates_path)

# Initialisation des use cases
repository = Base64RepositoryImpl()
base64_use_cases = Base64UseCases(repository)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil avec les deux outils"""
    seo_config = MetaGenerator.get_home_seo()
    encoding_categories = MetaGenerator.get_encoding_categories()
    context = PageContext(seo=seo_config, encoding_categories=encoding_categories)
    return templates.TemplateResponse(
        "base64_tool.html", {"request": request, "context": context}
    )


@router.get("/encode", response_class=HTMLResponse)
async def encode_form(request: Request):
    """Affiche le formulaire d'encodage (GET)"""
    seo_config = MetaGenerator.get_encode_seo()
    encoding_categories = MetaGenerator.get_encoding_categories()
    context = PageContext(seo=seo_config, encoding_categories=encoding_categories)
    return templates.TemplateResponse(
        "base64_tool.html", {"request": request, "context": context}
    )


@router.post("/encode", response_class=HTMLResponse)
async def encode_text(
    request: Request, plain_text: str = Form(...), character_set: str = Form("auto")
):
    """Traite l'encodage (POST)"""
    seo_config = MetaGenerator.get_encode_seo()
    encoding_categories = MetaGenerator.get_encoding_categories()
    encode_request = Base64EncodeRequest(text=plain_text, charset=character_set)
    result = await base64_use_cases.encode_text(encode_request)

    context = PageContext(
        seo=seo_config,
        encoded_result=result.result if result.success else "",
        encode_error=result.error if not result.success else "",
        original_text=plain_text,
        charset=character_set,
        encoding_categories=encoding_categories,
    )

    return templates.TemplateResponse(
        "base64_tool.html", {"request": request, "context": context}
    )


@router.get("/decode", response_class=HTMLResponse)
async def decode_form(request: Request):
    """Affiche le formulaire de décodage (GET)"""
    seo_config = MetaGenerator.get_decode_seo()
    encoding_categories = MetaGenerator.get_encoding_categories()
    context = PageContext(seo=seo_config, encoding_categories=encoding_categories)
    return templates.TemplateResponse(
        "base64_tool.html", {"request": request, "context": context}
    )


@router.post("/decode", response_class=HTMLResponse)
async def decode_base64(
    request: Request,
    base64_text: str = Form(...),
    character_set: str = Form("auto"),
    decode_line_by_line: bool = Form(False),
):
    """Traite le décodage (POST)"""
    seo_config = MetaGenerator.get_decode_seo()
    encoding_categories = MetaGenerator.get_encoding_categories()
    decode_request = Base64DecodeRequest(
        base64_text=base64_text,
        charset=character_set,
        decode_line_by_line=decode_line_by_line,
    )
    result = await base64_use_cases.decode_text(decode_request)

    context = PageContext(
        seo=seo_config,
        decoded_result=result.result if result.success else "",
        decode_error=result.error if not result.success else "",
        original_base64=base64_text,
        charset=character_set,
        decode_line_by_line=decode_line_by_line,
        encoding_categories=encoding_categories,
    )

    return templates.TemplateResponse(
        "base64_tool.html", {"request": request, "context": context}
    )


@router.get("/sitemap.xml")
async def sitemap(request: Request):
    """Endpoint sécurisé pour le sitemap XML"""
    try:
        base_url = str(request.base_url).rstrip("/")
        sitemap_content = SitemapGenerator.generate_sitemap(base_url)

        # Validation supplémentaire du contenu
        if SitemapGenerator.validate_sitemap_content(sitemap_content):
            return Response(
                content=sitemap_content,
                media_type="application/xml",
                headers={"Content-Disposition": "inline; filename=sitemap.xml"},
            )
        else:
            raise HTTPException(
                status_code=500, detail="Erreur de génération du sitemap"
            )

    except Exception as e:
        # Log l'erreur mais ne pas exposer les détails en production
        print(f"Erreur sitemap: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@router.get("/robots.txt")
async def robots(request: Request):
    """Endpoint pour robots.txt"""
    base_url = str(request.base_url).rstrip("/")
    content = f"""# Robots.txt pour Outils en Ligne
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Crawl-delay: 1

# Sitemaps
Sitemap: {base_url}/sitemap.xml"""

    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": "inline; filename=robots.txt"},
    )


class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    tool_suggestion: str | None = ""


@router.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    """Affiche le formulaire de contact"""
    seo_config = SEOConfig(
        title="Contact - Outils en Ligne",
        description="Contactez-nous pour des suggestions d'outils, des questions ou des retours. Nous sommes à votre écoute !",
        keywords="contact, suggestions outils, feedback, support, questions",
        canonical_url="/contact",
        og_title="Contact - Outils en Ligne",
        og_description="Contactez-nous pour des suggestions ou questions",
    )
    context = PageContext(seo=seo_config)
    return templates.TemplateResponse(
        "contact.html", {"request": request, "context": context}
    )


@router.post("/contact", response_class=HTMLResponse)
async def send_contact_message(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    tool_suggestion: str = Form(""),
):
    """Traite l'envoi du formulaire de contact"""
    try:
        # Validation basique de l'email
        if "@" not in email or "." not in email:
            raise HTTPException(status_code=400, detail="Email invalide")

        # Ici vous pourriez intégrer un service d'email comme SendGrid, Mailgun, etc.
        # Pour l'instant, nous allons simplement simuler l'envoi

        seo_config = SEOConfig(
            title="Message Envoyé - Outils en Ligne",
            description="Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.",
            keywords="message envoyé, contact réussi, confirmation",
            canonical_url="/contact",
            og_title="Message Envoyé - Outils en Ligne",
            og_description="Votre message a été envoyé avec succès",
        )

        context = PageContext(
            seo=seo_config,
            contact_success=True,
            original_name=name,
            original_email=email,
            original_subject=subject,
            original_message=message,
            original_tool_suggestion=tool_suggestion,
        )

        # Log du message (dans un vrai projet, enregistrez en base de données)
        print("📧 Nouveau message de contact:")
        print(f"   Nom: {name}")
        print(f"   Email: {email}")
        print(f"   Sujet: {subject}")
        print(f"   Message: {message}")
        if tool_suggestion:
            print(f"   Suggestion d'outil: {tool_suggestion}")

        return templates.TemplateResponse(
            "contact.html", {"request": request, "context": context}
        )

    except Exception as e:
        seo_config = SEOConfig(
            title="Erreur - Contact",
            description="Une erreur est survenue lors de l'envoi de votre message.",
            keywords="erreur contact, problème envoi",
            canonical_url="/contact",
            og_title="Erreur - Contact",
            og_description="Erreur lors de l'envoi du message",
        )

        context = PageContext(
            seo=seo_config,
            contact_error=f"Une erreur est survenue: {str(e)}",
            original_name=name,
            original_email=email,
            original_subject=subject,
            original_message=message,
            original_tool_suggestion=tool_suggestion,
        )

        return templates.TemplateResponse(
            "contact.html", {"request": request, "context": context}
        )
