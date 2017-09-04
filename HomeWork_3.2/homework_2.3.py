def detect_encoding(file):
    import chardet
    with open(file, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
    return result['encoding']


def open_file(file, file_encoding):
    import json
    with open(file, encoding=file_encoding) as f:
        news = json.load(f)
    return news


def analysis_news(news):
    title = news['rss']['channel']['title']
    news_text = ''
    for item in news['rss']['channel']['items']:  # Создаем строку со всеми новостями из файла
        news_text += (item['description'] + ' ')
    news_list = news_text.split()
    news_dct = {}
    for i in news_list:  # Считаем кол-во повторений каждого слова и заносим данные в словарь
        if len(i) > 5:  # Выбираем слова из новостей длиннее 6 символов
            if i in news_dct:
                news_dct[i] += 1
            else:
                news_dct[i] = 1
    # Упорядочим элементы словаря по значениям.
    news_list_sorted = sorted(news_dct.items(), key=lambda element: element[1], reverse=True)
    return title, news_list_sorted


def print_top10(title, news_list_sorted):
    print('Для файла:"{}" топ 10 слов:'.format(title))
    for idx, item in enumerate(news_list_sorted[:10]):
        print('{}. Слово - "{}" найдено {} раз'.format(idx + 1, item[0], item[1]))
    print()


def main():
    files_list = ['newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json']
    for file in files_list:
        file_encoding = detect_encoding(file)
        news = open_file(file, file_encoding)
        title, news_list_sorted = analysis_news(news)
        print_top10(title, news_list_sorted)


main()
