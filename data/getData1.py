#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simplejson as json
import requests
from decimal import Decimal
import datetime


def retrieveData(quoteTradingSymbol, baseTradingSymbol, tickInterval):
    BASE_URL = 'https://dev-api.shrimpy.io'
    API_ENDPOINT = '/v1/exchanges/binance/candles'
    url = "{}{}?quoteTradingSymbol={}&baseTradingSymbol={}&interval={}".format(
        BASE_URL,
        API_ENDPOINT,
        quoteTradingSymbol,
        baseTradingSymbol,
        tickInterval
    )
    return requests.get(url).json()


def transformData(entry):
    unixTime = int(datetime.datetime.strptime(
        entry['time'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
    openValue = Decimal(entry["open"])
    highValue = Decimal(entry["high"])
    lowValue = Decimal(entry["low"])
    closeValue = Decimal(entry["close"])
    volValue = Decimal(entry["volume"])
    return [unixTime, openValue, highValue, lowValue, closeValue, volValue]


def generateChartJson(chartData):
    result = {}
    result['chart'] = {
        "type": "Candles",
        "data": chartData,
        "settings": {}
    }
    return result


if __name__ == '__main__':
    api_data = retrieveData("BTC", "DCR", "1h")

    data = [transformData(entry) for entry in api_data]

    chartDictiory = generateChartJson(data)

    with open('data.json', "w+") as f:
        f.write(json.dumps(chartDictiory, indent=4))
