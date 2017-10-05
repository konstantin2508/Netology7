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


class Counter:

    stat_url = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_counter_visits(self, ):
        headers = self.get_headers()
        params = {
        'id': self.counter_id,
        'metrics': 'ym:s:visits'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']

    def get_counter_views(self, ):
        headers = self.get_headers()
        params = {
        'id': self.counter_id,
        'metrics': 'ym:s:pageviews'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']

    def get_counter_users(self, ):
        headers = self.get_headers()
        params = {
        'id': self.counter_id,
        'metrics': 'ym:s:users'
        }
        response = requests.get(self.stat_url, params, headers=headers)
        return response.json()['totals']


metrika = YandexMetrika(TOKEN)
counters = metrika.get_counters()
counter_id = counters[0]['id']

counter = Counter(TOKEN, counter_id)

print('Суммарное количество визитов:', counter.get_counter_visits())
print('Число просмотров страниц на сайте:', counter.get_counter_views())
print('Количество уникальных посетителей:', counter.get_counter_users())
