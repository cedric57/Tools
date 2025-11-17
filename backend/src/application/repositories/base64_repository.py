class Base64Repository:
    @staticmethod
    def encode(text: str) -> str:
        import base64

        encoded_bytes = base64.b64encode(text.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    @staticmethod
    def decode(encoded_text: str) -> str:
        import base64

        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode("utf-8")
