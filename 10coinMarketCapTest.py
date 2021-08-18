from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'fbe0bd89-adb2-47e3-9eb4-abea4a488d81'  # 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    init_message = json.loads(response.text)
    data = init_message['data']
    # print(data)

    index = 0
    for item in data:
        index += 1
        print("==============")
        print(item)
        if index > 2:
            break


except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
