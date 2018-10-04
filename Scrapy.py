import requests
from bs4 import BeautifulSoup
import sys
from twilio.rest import Client
import credentials

def Main():
    stock_list = ["CRON","N","ISOL:CNX","MGWFF:US"]
    client = Client(credentials.login['SID'],credentials.login['Auth'])

    for stock_ele in stock_list:
        try:
            if ":" in stock_ele:
                stock_ele_split = stock_ele.split(":")
                page = requests.get("https://web.tmxmoney.com/getquote.php?symbols%5B%5D={}%3A{}".format(stock_ele_split[0],stock_ele_split[1]))
            else:
                page = requests.get("https://web.tmxmoney.com/getquote.php?symbols%5B%5D={}".format(stock_ele))
        except requests.exceptions.Timeout as err:
            print(err)
            #TODO: Set up for retrying
        except requests.exceptions.TooManyRedirects as err:
            print(err)
            print("Skipping...")
            continue
        except requests.exceptions.RequestException as err:
            print(err)
            sys.exit(1)


        soup = BeautifulSoup(page.content,'html.parser')
        stock_info_list = [ele.get_text() for ele in soup.find_all('td')]
        print(stock_info_list)
        stock_symbol = stock_info_list[0]
        stock_name = stock_info_list[1]
        stock_price = stock_info_list[2]
        stock_price_change = stock_info_list[3]
        client.messages.create(to="19999999999",from_="+19999999999",body="{} {} \nPrice: {} Change: {}"
                               .format(stock_symbol,stock_name,stock_price,stock_price_change))




if __name__ == "__main__":
        Main()

