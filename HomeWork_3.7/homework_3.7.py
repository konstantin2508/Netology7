import requests

TOKEN = 'AQAAAAAgpX9gAASOAXvIDTYfmUUvtuE364wO7zo'


class YandexMetrika:
    management_url = 'https://api-metrika.yandex.ru/management/v1/counters'
    stat_url = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_counters(self):
        headers = self.get_headers()
        response = requests.get(self.management_url, headers=headers)
        return response.json()['counters']

    def get_counter_visits(self, counter_id, ):
        headers = self.get_headers()
        params = {
        'id': counter_id,
        'metrics': 'ym:s:visits'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']

    def get_counter_views(self, counter_id, ):
        headers = self.get_headers()
        params = {
        'id': counter_id,
        'metrics': 'ym:s:pageviews'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']

    def get_counter_users(self, counter_id, ):
        headers = self.get_headers()
        params = {
        'id': counter_id,
        'metrics': 'ym:s:users'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']

metrika = YandexMetrika(TOKEN)
counters = metrika.get_counters()
for counter in counters:
    print('По счетчику:', counter['name'], 'статистика составляет:')
    print('Суммарное количество визитов:', metrika.get_counter_visits(counter['id']))
    print('Число просмотров страниц на сайте:', metrika.get_counter_views(counter['id']))
    print('Количество уникальных посетителей:', metrika.get_counter_users(counter['id']))
