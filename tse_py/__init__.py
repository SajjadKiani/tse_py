import requests
import pandas as pd

# headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# define a base url
base_url = 'http://cdn.tsetmc.com/api/'

def buy_sell_history(stock_code):
    try:
        response = requests.get(base_url + 'BestLimits/' + str(stock_code), headers=headers)
        # convert to pandas dataframe
        df = pd.DataFrame(response.json()['bestLimits'])
        return df
    except Exception as e:
        return 'Error: ' + str(e)

def closing_price(stock_code):
    try:
        response = requests.get(base_url + 'ClosingPrice/GetClosingPriceInfo/' + str(stock_code), headers=headers)
        response = response.json()
        response['closingPriceInfo'].pop('instrumentState')
        return pd.DataFrame(response['closingPriceInfo'], index=[0])
    except Exception as e:
        return 'Error: ' + str(e)


def client_type(stock_code):
    try: 
        response = requests.get(base_url + 'ClientType/GetClientType/' + str(stock_code) + '/1/0', headers=headers)
        return pd.DataFrame(response.json()['clientType'], index=[0])
    except Exception as e:
        return 'Error: ' + str(e)
    
def get_time():
    try:
        response = requests.get(base_url + 'StaticData/GetTime', headers=headers)
        # TODO: convert to jalali
        return response.text
    except Exception as e:
        return 'Error: ' + str(e)




