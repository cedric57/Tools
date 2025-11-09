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
            # Vérifier si on doit décoder ligne par ligne
            if hasattr(request, "decode_line_by_line") and request.decode_line_by_line:
                return await self._decode_line_by_line(request)
            else:
                return await self._decode_single(request)

        except Exception as e:
            return Base64Response(
                success=False, error=f"Erreur de décodage: {str(e)}", original_input=request.base64_text
            )

    async def _decode_single(self, request: Base64DecodeRequest) -> Base64Response:
        """Décodage d'une seule chaîne Base64"""
        decoded_bytes = base64.b64decode(request.base64_text)

        # Gestion de l'auto-détection
        if request.charset == "auto":
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
                        success=True, result=f"[Encodage: UTF-8 (défaut)]\n{result}", original_input=request.base64_text
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

    async def _decode_line_by_line(self, request: Base64DecodeRequest) -> Base64Response:
        """Décodage ligne par ligne pour entrées multiples"""
        lines = request.base64_text.strip().split("\n")
        results = []
        error_lines = []

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # Ignorer les lignes vides
                continue

            try:
                decoded_bytes = base64.b64decode(line)

                # Gestion de l'encodage
                if request.charset == "auto":
                    detection = chardet.detect(decoded_bytes)
                    detected_encoding = detection["encoding"]
                    confidence = detection["confidence"]

                    if detected_encoding and confidence > 0.7:
                        charset = detected_encoding
                        decoded_text = decoded_bytes.decode(charset)
                        results.append(f"Ligne {i} [{detected_encoding} - {confidence:.2%}]: {decoded_text}")
                    else:
                        try:
                            decoded_text = decoded_bytes.decode("utf-8")
                            results.append(f"Ligne {i} [UTF-8]: {decoded_text}")
                        except:
                            decoded_text = decoded_bytes.decode("latin-1")
                            results.append(f"Ligne {i} [Latin-1]: {decoded_text}")
                else:
                    decoded_text = decoded_bytes.decode(request.charset)
                    results.append(f"Ligne {i}: {decoded_text}")

            except Exception as e:
                error_lines.append(f"Ligne {i}: ERREUR - {str(e)}")
                results.append(f"Ligne {i}: ❌ ERREUR - {line[:50]}{'...' if len(line) > 50 else ''}")

        # Construire le résultat final
        result_parts = []

        if results:
            result_parts.append("✅ DÉCODAGE LIGNE PAR LIGNE:")
            result_parts.extend(results)

        if error_lines:
            result_parts.append("\n❌ ERREURS:")
            result_parts.extend(error_lines)

        if not results and not error_lines:
            return Base64Response(
                success=False, error="Aucune ligne valide à décoder", original_input=request.base64_text
            )

        final_result = "\n".join(result_parts)

        # Ajouter un résumé
        total_lines = len([l for l in lines if l.strip()])
        successful_lines = len(results) - len(error_lines)

        summary = f"\n\n📊 RÉSUMÉ: {successful_lines}/{total_lines} lignes décodées avec succès"
        if error_lines:
            summary += f", {len(error_lines)} erreurs"

        final_result += summary

        return Base64Response(success=True, result=final_result, original_input=request.base64_text)
