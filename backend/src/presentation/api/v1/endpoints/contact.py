from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    tool_suggestion: str | None = None


class ContactResponse(BaseModel):
    success: bool
    message_id: str | None = None
    error: str | None = None


@router.post("/send", response_model=ContactResponse)
async def send_contact_message(request: ContactRequest):
    """Envoie un message de contact"""
    try:
        # Simulation d'envoi d'email
        # Dans un vrai projet, intégrez un service comme SendGrid, Mailgun, etc.
        print("📧 Nouveau message de contact:")
        print(f"   Nom: {request.name}")
        print(f"   Email: {request.email}")
        print(f"   Sujet: {request.subject}")
        print(f"   Message: {request.message}")
        if request.tool_suggestion:
            print(f"   Suggestion: {request.tool_suggestion}")

        # Générer un ID de message simulé
        import uuid

        message_id = str(uuid.uuid4())

        return ContactResponse(success=True, message_id=message_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'envoi du message: {str(e)}")
