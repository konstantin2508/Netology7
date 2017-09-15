import osa
import os
from math import ceil


# Переводит температуру из Фаренгейта в Цельсий и выводит среднюю
def convert_temp(temp_file_path):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    with open(temp_file_path) as f:
        temp_fahr_list = []
        for line in f:
            temp_fahr_list.append(line.strip().replace(' F', ''))
    temp_cels_list = []
    for temp in temp_fahr_list:
        response = client.service.ConvertTemp(temp, FromUnit='degreeFahrenheit', ToUnit='degreeCelsius')
        temp_cels = round(response, 1)
        temp_cels_list.append(temp_cels)
    return (sum(temp_cels_list) / len(temp_cels_list))


# Перевод валюты в рубли
def currencies(curr_file_path):
    client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    with open(curr_file_path) as f:
        costs_list = []
        for line in f:
            costs_list.append(line.strip().split())
    costs_rub = 0
    for costs in costs_list:
        response = client.service.ConvertToNum(toCurrency='RUB', fromCurrency=costs[2], amount=costs[1], rounding=True)
        costs_rub += response
    return costs_rub


# Перевод миль в км
def travel_unit(travel_file_path):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    with open(travel_file_path) as f:
        travel_list = []
        for line in f:
            travel_list.append(line.strip().split())
    travel_km = 0
    for travel in travel_list:
        response = client.service.ChangeLengthUnit(travel[1].replace(',', ''), fromLengthUnit='Miles', toLengthUnit='Kilometers')
        travel_km += round(response, 2)
    return travel_km


def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    temp_file = 'temps.txt'
    temp_file_path = os.path.join(current_dir, temp_file)
    temp_average = convert_temp(temp_file_path)
    print('Средняя за неделю температура по Цельсию состовляет:', temp_average)

    currencies_file = 'currencies.txt'
    curr_file_path = os.path.join(current_dir, currencies_file)
    costs_rub = ceil(currencies(curr_file_path))
    print('На путешествие вы потратите в рублях:', costs_rub)

    travel_file = 'travel.txt'
    travel_file_path = os.path.join(current_dir, travel_file)
    travel_km = travel_unit(travel_file_path)
    print('Суммарное растояние пути в км:', travel_km)

main()
