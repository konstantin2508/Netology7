import requests


def get_my_friends(**params):
    response = requests.get('https://api.vk.com/method/friends.get', params)
    list_friends = response.json()['response']['items']
    return list_friends


def print_list_my_friends(list_friends):
        for i, friend in enumerate(list_friends):
            print(i + 1, friend['first_name'], friend['last_name'])


def intersection_friends(list_id_all):
    for i, list_id in enumerate(list_id_all):
        if i == 0:
            set_friends = set(list_id)
        else:
            set_friends = set_friends & set(list_id)
    return set_friends


def start_menu():
    print("""
            Основное меню:
            1 - Получите список всех своих друзей
            2 - Для каждого своего друга получите список его друзей
            3 - Найдите пересечения (общих друзей) между всеми пользователями
            """)
    input_command = None
    while input_command not in ['1', '2', '3', '']:
        input_command = input('Выберите команду (для выхода нажмите Enter):')
        if input_command not in ['1', '2', '3', '']:
            print('Такой команды нет в программе!!!')
    return input_command


def main():
    access_token = '83899a92f6dc493fbcc2bb98caaea7284062ad705097b939271ba9738396dfd144e2b957ae65966a2e9a0'
    params = {
        'access_token': access_token,
        'v': '5.68',
        'fields': 'nickname'
    }
    choice = start_menu()
    while choice:
        if choice == '1':
            # Получите список всех своих друзей
            list_friends = get_my_friends(access_token=params['access_token'], v=params['v'], fields=params['fields'])
            print('Список моих друзей:')
            print_list_my_friends(list_friends)
            choice = start_menu()
        elif choice == '2':
            # Для каждого своего друга получите список его друзей
            print('Подождите...Идет обработка запроса...')
            list_friends = get_my_friends(access_token=params['access_token'], v=params['v'], fields=params['fields'])
            for friend in list_friends:
                list_friends_friends = get_my_friends(access_token=params['access_token'], v=params['v'],
                                                      fields=params['fields'], user_id=friend['id'])
                print('Список друзей:', friend['first_name'], friend['last_name'])
                print_list_my_friends(list_friends_friends)
                print()
            choice = start_menu()
        elif choice == '3':
            # Получаем список всех друзей моих друзей
            print('Подождите...Идет обработка запроса...')
            list_friends = get_my_friends(access_token=params['access_token'], v=params['v'], fields=params['fields'])
            list_id_all = []
            for friend in list_friends:
                list_friends_friends = get_my_friends(access_token=params['access_token'], v=params['v'],
                                                     fields=params['fields'], user_id=friend['id'])
                list_id = []
                for i in list_friends_friends:
                    list_id.append(i['id'])
                list_id_all.append(list_id)

            # Находим пересечение общих друзей
            set_friends = intersection_friends(list_id_all)

            # Находим пользователя по user_id
            for friend in set_friends:
                params['user_ids'] = int(friend)
                response = requests.get('https://api.vk.com/method/users.get', params)
                print('Общие друзья:')
                for id in response.json()['response']:
                    print(id['first_name'], id['last_name'])
            choice = start_menu()

    print('До свидания!')


main()
