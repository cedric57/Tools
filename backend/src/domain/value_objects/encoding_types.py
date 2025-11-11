from enum import Enum


class EncodingCategory(str, Enum):
    AUTO_DETECT = "AUTO-DETECT"
    POPULAR = "POPULAR"
    OTHER = "OTHER"


class EncodingTypes:
    @staticmethod
    def get_encoding_categories() -> list[tuple[str, list[tuple[str, str]]]]:
        return [
            (EncodingCategory.AUTO_DETECT, [("auto", "Auto-détection (Recommandé)")]),
            (
                EncodingCategory.POPULAR,
                [
                    ("utf-8", "UTF-8 (Unicode)"),
                    ("ascii", "ASCII"),
                    ("latin-1", "ISO-8859-1 (Latin-1)"),
                    ("windows-1252", "Windows-1252"),
                    ("utf-16", "UTF-16"),
                ],
            ),
            (
                EncodingCategory.OTHER,
                [
                    ("utf-32", "UTF-32"),
                    ("utf-7", "UTF-7"),
                    ("iso-8859-15", "ISO-8859-15 (Latin-9)"),
                    ("windows-1251", "Windows-1251 (Cyrillique)"),
                    ("shift_jis", "Shift JIS (Japonais)"),
                    ("euc-kr", "EUC-KR (Coréen)"),
                    ("gb2312", "GB2312 (Chinois simplifié)"),
                    ("big5", "Big5 (Chinois traditionnel)"),
                    ("koi8-r", "KOI8-R (Russe)"),
                ],
            ),
        ]
