import requests
import os
import chardet


def translate_it(file_input, file_output, lang_input, lang_output):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    with open(file_input, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        text = data.decode(result['encoding'])

    lang = lang_input + '-' + lang_output
    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }

    response = requests.get(url, params=params).json()

    with open(file_output, 'w') as document:
        document.write(' '.join(response.get('text', [])))

    return ' '.join(response.get('text', []))


def create_list_files_translation(list_files):
    list_files_translation = []
    for file in list_files:
        if file.endswith('.txt'):
            list_files_translation.append(file)
    return list_files_translation


def choice_lang(text_input):
    print("""
        Выберите язык для перевода:
        1 - французский
        2 - испанский
        3 - немецкий
        """)
    choice = None
    lang = None
    while choice not in ['1', '2', '3', '']:
        choice = input(text_input)
        if choice == '1':
            lang = 'fr'
        elif choice == '2':
            lang = 'es'
        elif choice == '3':
            lang = 'de'
        elif choice == '':
            lang = 'ru'
        else:
            print('Такого языка нет в нашем словаре!!!')
    return lang


def main():
    result = 'Translated'  # задаем имя папки для сохранения переведенных файлов
    current_dir = os.path.dirname(os.path.abspath(__file__))  # определяем рабочий каталог
    translated_dir = os.path.join(current_dir, result)  # путь к папке с переведенными файлами
    # проверяем наличие папки для сохранения переведенных файлов, если нет создаем
    if not os.path.exists(translated_dir):
        os.mkdir(translated_dir)

    list_files = os.listdir(current_dir)
    list_files_translation = create_list_files_translation(list_files)  # создаем список файлов для перевода
    for file in list_files_translation:
        print('Переводим текст в файле:', file)
        lang_input = choice_lang('Выберите с какого языка переводим (при нажатии Enter - по умолчанию русский):')
        lang_output = choice_lang('Выберите на какой язык переводим (при нажатии Enter - по умолчанию русский):')
        print('Подождите...Идет обработка файла...')
        translate_it(os.path.join(current_dir, file), os.path.join(translated_dir, file), lang_input, lang_output)


main()
