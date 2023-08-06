import requests
import pandas as pd
from persiantools.jdatetime import JalaliDate
from persiantools import characters
import re

# headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# define a base url
base_url = 'http://cdn.tsetmc.com/api/'


def __Get_TSE_WebID__(stock):
    # search TSE function ------------------------------------------------------------------------------------------------------------
    def request(name):
        page = requests.get(f'http://old.tsetmc.com/tsev2/data/search.aspx?skey={name}', headers=headers)
        data = []
        for i in page.text.split(';') :
            try :
                i = i.split(',')
                data.append([i[0],i[1],i[2],i[7],i[-1]])
            except :
                pass
        data = pd.DataFrame(data, columns=['Ticker','Name','WEB-ID','Active','Market'])
        data['Name'] = data['Name'].apply(lambda x : characters.ar_to_fa(' '.join([i.strip() for i in x.split('\u200c')]).strip()))
        data['Ticker'] = data['Ticker'].apply(lambda x : characters.ar_to_fa(''.join(x.split('\u200c')).strip()))
        data['Name-Split'] = data['Name'].apply(lambda x : ''.join(x.split()).strip())
        data['Symbol-Split'] = data['Ticker'].apply(lambda x : ''.join(x.split()).strip())
        data['Active'] = pd.to_numeric(data['Active'])
        data = data.sort_values('Ticker')
        data = pd.DataFrame(data[['Name','WEB-ID','Name-Split','Symbol-Split','Market']].values, columns=['Name','WEB-ID',
                            'Name-Split','Symbol-Split','Market'], index=pd.MultiIndex.from_frame(data[['Ticker','Active']]))
        return data
    #---------------------------------------------------------------------------------------------------------------------------------
    if type(stock) != str:
        print('Please Enetr a Valid Ticker or Name!')
        return False
    if(stock=='آ س پ'):
        stock = 'آ.س.پ'
    # cleaning input search key
    stock = characters.ar_to_fa(''.join(stock.split('\u200c')).strip())
    first_name = stock.split()[0]
    stock = ''.join(stock.split())
    # search TSE and process:
    data = request(first_name)
    df_symbol = data[data['Symbol-Split'] == stock]
    df_name = data[data['Name-Split'] == stock]
    if len(df_symbol) > 0 :
        df_symbol = df_symbol.sort_index(level=1,ascending=False).drop(['Name-Split','Symbol-Split'], axis=1)
        df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
        df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                       'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
        df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
        return df_symbol
    elif len(df_name) > 0 :
        symbol = df_name.index[0][0]
        data = request(symbol)
        symbol = characters.ar_to_fa(''.join(symbol.split('\u200c')).strip())
        df_symbol = data[data.index.get_level_values('Ticker') == symbol]
        if len(df_symbol) > 0 :
            df_symbol = df_symbol.sort_index(level=1,ascending=False).drop(['Name-Split','Symbol-Split'], axis=1)
            df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
            df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                           'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
            df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
            return df_symbol
    print('Please Enetr a Valid Ticker or Name!')
    return False

def buy_sell_history(stock_name: str):
    stock_code = __Get_TSE_WebID__(stock_name)['WEB-ID'][0]
    if (type(stock_code) == bool):
        return stock_code
    try:
        response = requests.get(base_url + 'BestLimits/' + str(stock_code), headers=headers)
        # convert to pandas dataframe
        df = pd.DataFrame(response.json()['bestLimits'])
        return df
    except Exception as e:
        return 'Error: ' + str(e)

def closing_price(stock_name: str):
    stock_code = __Get_TSE_WebID__(stock_name)['WEB-ID'][0]
    if (type(stock_code) == bool):
        return stock_code
    try:
        response = requests.get(base_url + 'ClosingPrice/GetClosingPriceInfo/' + str(stock_code), headers=headers)
        response = response.json()
        response['closingPriceInfo'].pop('instrumentState')
        return pd.DataFrame(response['closingPriceInfo'], index=[0])
    except Exception as e:
        return 'Error: ' + str(e)


def client_type(stock_name: str):
    stock_code = __Get_TSE_WebID__(stock_name)['WEB-ID'][0]
    if (type(stock_code) == bool):
        return stock_code
    try: 
        response = requests.get(base_url + 'ClientType/GetClientType/' + str(stock_code) + '/1/0', headers=headers)
        return pd.DataFrame(response.json()['clientType'], index=[0])
    except Exception as e:
        return 'Error: ' + str(e)
    
def get_time():
    try:
        response = requests.get(base_url + 'StaticData/GetTime', headers=headers)

        jalali_date = JalaliDate.to_jalali(pd.to_datetime(response.text, utc=True).tz_convert('Asia/Tehran')).strftime('%Y/%m/%d')
        time = pd.to_datetime(response.text, utc=True).tz_convert('Asia/Tehran').time().strftime('%H:%M:%S')
        return (jalali_date , time)

        # return response.text
    except Exception as e:
        return 'Error: ' + str(e)



