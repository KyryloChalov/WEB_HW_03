""" translation for cyrillic symbols in filename"""

from pathlib import Path

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "jo",
    "zh",
    "z",
    "y",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "`",
    "y",
    "'",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
for c, literal in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[c] = literal
    TRANS[c.upper()] = literal.upper()


def normalize(file_name: str) -> str:
    """
    Функція normalize:
    Проводить транслітерацію кириличного алфавіту на латинський.
    Замінює всі символи, крім латинських літер та цифр, на '_'.
    Вимоги до функції normalize:
    приймає на вхід рядок та повертає рядок;
    проводить транслітерацію кириличних символів на латиницю;
    замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
    транслітерація може не відповідати стандарту, але бути читабельною;
    великі літери залишаються великими, а маленькі — маленькими після транслітерації.
    """

    result = ""
    name = str(Path(file_name).stem)
    name_len = len(name)

    for i in range(name_len):
        if any(["0" <= name[i] <= "9", "a" <= name[i] <= "z", "A" <= name[i] <= "Z"]):
            result += name[i]
        elif name[i] in TRANS:  # cyrillic
            result += TRANS[name[i]]
        else:
            result += "_"

    return result + str(Path(file_name).suffix)
