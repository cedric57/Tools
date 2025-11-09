import base64

import chardet

from ...core.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response
from ...core.ports.base64_repository import Base64Repository


class Base64RepositoryImpl(Base64Repository):
    async def encode(self, request: Base64EncodeRequest) -> Base64Response:
        try:
            # Gestion de l'auto-détection pour l'encodage
            if request.charset == "auto":
                # Pour l'encodage, on utilise UTF-8 par défaut pour l'auto-détection
                charset = "utf-8"
            else:
                charset = request.charset

            encoded_bytes = request.text.encode(charset)
            result = base64.b64encode(encoded_bytes).decode("ascii")
            return Base64Response(success=True, result=result, original_input=request.text)
        except Exception as e:
            return Base64Response(success=False, error=f"Erreur d'encodage: {str(e)}", original_input=request.text)

    async def decode(self, request: Base64DecodeRequest) -> Base64Response:
        try:
            decoded_bytes = base64.b64decode(request.base64_text)

            # Gestion de l'auto-détection
            if request.charset == "auto":
                # Détection automatique de l'encodage
                detection = chardet.detect(decoded_bytes)
                detected_encoding = detection["encoding"]
                confidence = detection["confidence"]

                if detected_encoding and confidence > 0.7:
                    charset = detected_encoding
                    result = decoded_bytes.decode(charset)
                    return Base64Response(
                        success=True,
                        result=f"[Auto-détection: {detected_encoding} - Confiance: {confidence:.2%}]\n{result}",
                        original_input=request.base64_text,
                    )
                else:
                    # Essayer UTF-8 par défaut si la détection échoue
                    try:
                        result = decoded_bytes.decode("utf-8")
                        return Base64Response(
                            success=True,
                            result=f"[Encodage: UTF-8 (défaut)]\n{result}",
                            original_input=request.base64_text,
                        )
                    except:
                        # Dernier recours: latin-1 qui ne échoue jamais
                        result = decoded_bytes.decode("latin-1")
                        return Base64Response(
                            success=True,
                            result=f"[Encodage: Latin-1 (fallback)]\n{result}",
                            original_input=request.base64_text,
                        )
            else:
                # Utiliser l'encodage spécifié
                result = decoded_bytes.decode(request.charset)
                return Base64Response(success=True, result=result, original_input=request.base64_text)

        except Exception as e:
            return Base64Response(
                success=False, error=f"Erreur de décodage: {str(e)}", original_input=request.base64_text
            )
