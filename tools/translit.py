table_ru_eng = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': ('e', 'ye', 'аоиеёэыуюя'),
    'ё': ('e', 'ye', 'аоиеёэыуюя'),
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_',
}


def translit_it(source: str) -> str:
    """
    Transliterate russian characters to english
    :param source: String with russian characters
    :return: transliterated string
    """
    old_symbol = None
    first_letter = True
    strings = list(source)
    result = list()

    while strings:
        symbol = str(strings.pop(0))
        tr_symb = table_ru_eng.get(symbol.lower(), symbol)
        if type(tr_symb) is tuple:
            if first_letter:
                guess = tr_symb[1]
            else:
                if old_symbol in tr_symb[2]:
                    guess = tr_symb[1]
                else:
                    guess = tr_symb[0]
        else:
            guess = tr_symb
        old_symbol = symbol
        first_letter = False
        if symbol.isupper():
            guess = guess.capitalize()
        result.append(guess)
    return ''.join(result)
