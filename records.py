import csv
import json
from os import write
from datetime import date

def check_records(stocks):
    stocks_to_buy = []

    for stock in stocks:
        with open('current_holdings.json','r') as json_file:
            data = json_file.read()
            jsonObj = json.loads(data)

            try:
                jsonObj[stock]
            except:
                stocks_to_buy.append(stock)
            else:
                print("already holding " + stock)
    
    return stocks_to_buy


def update_buys(stocks):

    row_list = []

    for stock in stocks:
        list_item = [date.today(), stock]
        row_list.append(list_item)

    with open('test.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file)
        for row in row_list:
            writer.writerow(row)


def update_current_holdings(stocks):

    row_list = []

    for stock in stocks:
        row_list.append(stock)

    list_of_list = [[el] for el in row_list]

    with open('test.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file)
        for row in list_of_list:
            writer.writerow(row)
