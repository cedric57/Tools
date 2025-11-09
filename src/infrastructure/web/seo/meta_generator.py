from ....application.dto.base64_dto import EncodingCategory, SEOConfig


class MetaGenerator:
    @staticmethod
    def get_encoding_categories() -> list[EncodingCategory]:
        return [
            EncodingCategory(
                name="AUTO-DETECT",
                encodings=[
                    ("auto", "Auto-détection (Recommandé)"),
                ],
            ),
            EncodingCategory(
                name="Populaires",
                encodings=[
                    ("utf-8", "UTF-8 (Unicode)"),
                    ("ascii", "ASCII"),
                    ("latin-1", "ISO-8859-1 (Latin-1)"),
                    ("windows-1252", "Windows-1252"),
                    ("utf-16", "UTF-16"),
                ],
            ),
            EncodingCategory(
                name="Autres",
                encodings=[
                    ("utf-32", "UTF-32"),
                    ("utf-7", "UTF-7"),
                    ("iso-8859-15", "ISO-8859-15 (Latin-9)"),
                    ("windows-1251", "Windows-1251 (Cyrillique)"),
                    ("windows-1256", "Windows-1256 (Arabe)"),
                    ("shift_jis", "Shift JIS (Japonais)"),
                    ("euc-jp", "EUC-JP (Japonais)"),
                    ("iso-2022-jp", "ISO-2022-JP (Japonais)"),
                    ("euc-kr", "EUC-KR (Coréen)"),
                    ("gb2312", "GB2312 (Chinois simplifié)"),
                    ("gbk", "GBK (Chinois)"),
                    ("big5", "Big5 (Chinois traditionnel)"),
                    ("koi8-r", "KOI8-R (Russe)"),
                    ("koi8-u", "KOI8-U (Ukrainien)"),
                    ("iso-8859-2", "ISO-8859-2 (Latin-2)"),
                    ("iso-8859-3", "ISO-8859-3 (Latin-3)"),
                    ("iso-8859-4", "ISO-8859-4 (Latin-4)"),
                    ("iso-8859-5", "ISO-8859-5 (Cyrillique)"),
                    ("iso-8859-6", "ISO-8859-6 (Arabe)"),
                    ("iso-8859-7", "ISO-8859-7 (Grec)"),
                    ("iso-8859-8", "ISO-8859-8 (Hébreu)"),
                    ("iso-8859-9", "ISO-8859-9 (Latin-5)"),
                    ("iso-8859-13", "ISO-8859-13 (Latin-7)"),
                    ("iso-8859-14", "ISO-8859-14 (Latin-8)"),
                    ("iso-8859-16", "ISO-8859-16 (Latin-10)"),
                    ("mac_roman", "Mac Roman"),
                    ("mac_cyrillic", "Mac Cyrillique"),
                ],
            ),
        ]

    @staticmethod
    def get_home_seo() -> SEOConfig:
        return SEOConfig(
            title="Encodeur et Décodeur Base64 en Ligne - Outil Gratuit",
            description="Outil en ligne gratuit pour encoder et décoder le Base64. Conversion rapide et sécurisée sans conservation des données. Support UTF-8, ASCII, Latin-1 et 30+ encodages.",
            keywords="base64, encodeur base64, décodeur base64, conversion base64, encodeur en ligne, décodeur en ligne, utf-8, ascii, auto-détection encodage",
            canonical_url="/",
            og_title="Encodeur/Décodeur Base64 - Outil Gratuit",
            og_description="Encodez et décodez le Base64 en ligne gratuitement avec support de 30+ encodages",
        )

    @staticmethod
    def get_encode_seo() -> SEOConfig:
        return SEOConfig(
            title="Encoder en Base64 - Outil en Ligne Gratuit",
            description="Encodez votre texte en Base64 facilement avec notre outil en ligne. Support multiple encodages de caractères incluant UTF-8, ASCII, Latin-1 et auto-détection.",
            keywords="encoder base64, texte vers base64, conversion base64, encodeur en ligne, encodage automatique",
            canonical_url="/encode",
            og_title="Encoder en Base64 - Outil Gratuit",
            og_description="Encodez votre texte en Base64 en un clic avec support multi-encodage",
        )

    @staticmethod
    def get_decode_seo() -> SEOConfig:
        return SEOConfig(
            title="Décoder le Base64 - Outil en Ligne Gratuit",
            description="Décodez votre Base64 en texte lisible facilement avec notre outil en ligne. Conversion rapide et précise avec auto-détection d'encodage et support de 30+ formats.",
            keywords="decoder base64, base64 vers texte, décodeur base64, décoder en ligne, auto-détection encodage",
            canonical_url="/decode",
            og_title="Décoder le Base64 - Outil Gratuit",
            og_description="Décodez votre Base64 en texte lisible avec auto-détection d'encodage",
        )
