import base64
import uuid
from datetime import date

import chardet

from application.repositories.base64_repository import Base64Repository
from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response


class Base64Operations:
    def __init__(self, repository: Base64Repository):
        self.repository = repository
        self.analytics_data = {
            "total_operations": 0,
            "encode_operations": 0,
            "decode_operations": 0,
            "encoding_usage": {},
            "daily_operations": {},
        }

    def encode_text(self, request: Base64EncodeRequest) -> Base64Response:
        try:
            # Gestion de l'auto-détection pour l'encodage
            charset = "utf-8" if request.charset == "auto" else request.charset

            encoded_bytes = request.text.encode(charset)
            result = base64.b64encode(encoded_bytes).decode("ascii")

            # Enregistrement pour analytics
            self._record_operation("encode", charset)

            return Base64Response(
                success=True,
                result=result,
                original_input=request.text,
                encoding_used=charset,
                operation_id=str(uuid.uuid4()),
            )
        except Exception as e:
            return Base64Response(success=False, error=f"Erreur d'encodage: {str(e)}", original_input=request.text)

    def decode_text(self, request: Base64DecodeRequest) -> Base64Response:
        try:
            if request.decode_line_by_line:
                return self._decode_line_by_line(request)
            else:
                return self._decode_single(request)

        except Exception as e:
            return Base64Response(
                success=False, error=f"Erreur de décodage: {str(e)}", original_input=request.base64_text
            )

    def _decode_single(self, request: Base64DecodeRequest) -> Base64Response:
        decoded_bytes = base64.b64decode(request.base64_text)

        if request.charset == "auto":
            detection = chardet.detect(decoded_bytes)
            detected_encoding = detection["encoding"]
            confidence = detection["confidence"]

            if detected_encoding and confidence > 0.7:
                charset = detected_encoding
                result = decoded_bytes.decode(charset)
                encoding_info = f"Auto-détection: {detected_encoding} ({confidence:.2%})"
            else:
                try:
                    result = decoded_bytes.decode("utf-8")
                    encoding_info = "UTF-8 (défaut)"
                    charset = "utf-8"
                except:
                    result = decoded_bytes.decode("latin-1")
                    encoding_info = "Latin-1 (fallback)"
                    charset = "latin-1"
        else:
            result = decoded_bytes.decode(request.charset)
            encoding_info = request.charset
            charset = request.charset

        # Enregistrement pour analytics
        self._record_operation("decode", charset)

        return Base64Response(
            success=True,
            result=f"{result}",
            original_input=request.base64_text,
            encoding_used=encoding_info,
            operation_id=str(uuid.uuid4()),
        )

    def _decode_line_by_line(self, request: Base64DecodeRequest) -> Base64Response:
        lines = request.base64_text.strip().split("\n")
        results = []
        error_lines = []

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                decoded_bytes = base64.b64decode(line)

                if request.charset == "auto":
                    detection = chardet.detect(decoded_bytes)
                    detected_encoding = detection["encoding"]

                    if detected_encoding and detection["confidence"] > 0.7:
                        charset = detected_encoding
                        decoded_text = decoded_bytes.decode(charset)
                        results.append(f"Ligne {i} [{detected_encoding}]: {decoded_text}")
                    else:
                        try:
                            decoded_text = decoded_bytes.decode("utf-8")
                            results.append(f"Ligne {i} [UTF-8]: {decoded_text}")
                            charset = "utf-8"
                        except:
                            decoded_text = decoded_bytes.decode("latin-1")
                            results.append(f"Ligne {i} [Latin-1]: {decoded_text}")
                            charset = "latin-1"
                else:
                    decoded_text = decoded_bytes.decode(request.charset)
                    results.append(f"Ligne {i}: {decoded_text}")
                    charset = request.charset

                # Enregistrement pour analytics
                self._record_operation("decode", charset)

            except Exception as e:
                error_lines.append(f"Ligne {i}: ERREUR - {str(e)}")
                results.append(f"Ligne {i}: ❌ ERREUR")

        # Construire le résultat final
        if not results and not error_lines:
            return Base64Response(
                success=False, error="Aucune ligne valide à décoder", original_input=request.base64_text
            )

        result_parts = []
        if results:
            result_parts.append("✅ DÉCODAGE LIGNE PAR LIGNE:")
            result_parts.extend(results)

        if error_lines:
            result_parts.append("\n❌ ERREURS:")
            result_parts.extend(error_lines)

        summary = f"\n\n📊 RÉSUMÉ: {len(results) - len(error_lines)}/{len(results)} lignes décodées"
        if error_lines:
            summary += f", {len(error_lines)} erreurs"

        final_result = "\n".join(result_parts) + summary

        return Base64Response(
            success=True,
            result=final_result,
            original_input=request.base64_text,
            encoding_used="Multiple",
            operation_id=str(uuid.uuid4()),
        )

    def _record_operation(self, operation_type: str, encoding: str):
        """Enregistre une opération pour les analytics"""
        self.analytics_data["total_operations"] += 1

        if operation_type == "encode":
            self.analytics_data["encode_operations"] += 1
        else:
            self.analytics_data["decode_operations"] += 1

        # Suivi de l'usage des encodages
        if encoding in self.analytics_data["encoding_usage"]:
            self.analytics_data["encoding_usage"][encoding] += 1
        else:
            self.analytics_data["encoding_usage"][encoding] = 1

        # Suivi quotidien
        today = date.today().isoformat()
        if today in self.analytics_data["daily_operations"]:
            self.analytics_data["daily_operations"][today] += 1
        else:
            self.analytics_data["daily_operations"][today] = 1

    def get_analytics(self):
        """Retourne les données d'analytics"""
        most_used_encoding = max(
            self.analytics_data["encoding_usage"].items(), key=lambda x: x[1], default=("utf-8", 0)
        )[0]

        today = date.today().isoformat()
        operations_today = self.analytics_data["daily_operations"].get(today, 0)

        return {
            "total_operations": self.analytics_data["total_operations"],
            "encode_operations": self.analytics_data["encode_operations"],
            "decode_operations": self.analytics_data["decode_operations"],
            "most_used_encoding": most_used_encoding,
            "operations_today": operations_today,
            "encoding_usage": self.analytics_data["encoding_usage"],
        }
