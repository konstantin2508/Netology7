import requests
import time
import codecs
import json


def get_groups(**params):
    response = requests.get('https://api.vk.com/method/groups.get', params)
    try:
        list_groups = [n['screen_name'] for n in response.json()['response']['items']]
    except:
        # Проверка, если один из друзей пользователя помечен как “удалён” или “заблокирован”
        if response.json()['error']['error_code'] == 7 or response.json()['error']['error_code'] == 18:
            list_groups = []
    return list_groups


def get_my_friends(**params):
    response = requests.get('https://api.vk.com/method/friends.get', params)
    count_friends = response.json()['response']['count']
    list_friends = response.json()['response']['items']
    return count_friends, list_friends


def get_userid(**params):
    response = requests.get('https://api.vk.com/method/users.get', params)
    try:
        user_id = response.json()['response'][0]['id']
    except:
        user_id = response.json()['error']['error_msg']
    return user_id


def get_group_info(**params):
    response = requests.get('https://api.vk.com/method/groups.getById', params)
    group_info = response.json()['response']
    return group_info


def out_data(groups_info):
    data_output = []
    for group in groups_info:
        data_output.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})
    with codecs.open('data.json', 'w', 'utf8') as outfile:
        outfile.write(json.dumps(data_output, sort_keys=True, ensure_ascii=False))
        print('Файл с выходными данными успешно создан!')


def start_menu():
    print("""
            Дипломная работа: “Шпионские игры”:
            1 - Ввести имя пользователя или его id в ВК
            """)
    choice = None
    while choice not in ['1', '']:
        choice = input('Выберите команду (для выхода нажмите Enter):')
        if choice not in ['1', '']:
            print('Такой команды нет в программе!!!')
    return choice


def main():
    access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
    params = {
        'access_token': access_token,
        'v': '5.68',
        'extended': '1',
        'fields': 'members_count'
    }

    choice = start_menu()
    while choice:
        if choice == '1':
            user = input('Введите имя пользователя или его id в ВК, для которого мы проводим исследование:')
            user_id = get_userid(**params, user_ids=user, name_case='Nom')
            if user_id == 'Invalid user id':
                print('Пользователя с таким именем в ВК не сущетвует!')
            else:
                params['user_id'] = user_id

                # Получаем список групп нашего пользователя
                list_groups = get_groups(**params)

                # Получаем список друзей
                count_friends, list_friends = get_my_friends(**params)

                # Получаем список групп для каждого друга
                list_groups_all_friends = []
                print('Ждите. Идет запрос... ')
                for i, friend in enumerate(list_friends):
                    params['user_id'] = friend['id']
                    list_groups_friends = get_groups(**params)
                    if not i % 10:
                        print('Ждите. Идет запрос...Обработано {} друзей из {}'.format(i, count_friends))
                    # Ограничение от ВК: не более 3х обращений к API в секунду
                    if not i % 3:
                        time.sleep(1)
                    list_groups_all_friends.append(list_groups_friends)

                # Форматируем список генератором списков
                list_groups_all_friends = [y for x in list_groups_all_friends for y in x]
                # Создаем множество из полученного списка групп друзей нашего пользователя
                set_groups_all_friends = set(list_groups_all_friends)
                # Создаем множество из списка групп нашего пользователя
                set_groups = set(list_groups)
                # Список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей
                set_groups = set_groups - set_groups_all_friends
                groups = str(set_groups).replace('\'', '')
                groups_info = get_group_info(access_token=params['access_token'], v=params['v'], group_ids=groups[1:-1],
                                             fields='members_count')
                # Выводим данные в файл data.json в нужном формате
                out_data(groups_info)

            choice = start_menu()

    print('До свидания!')

main()
