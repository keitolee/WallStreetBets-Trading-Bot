import csv
from os import write
from datetime import date

def check_records(stocks):
    count = 0
    stocks_to_buy = []

    for stock in stocks:
        current_ticker = stock[0]
        already_holding = False

        with open('current_holdings.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if current_ticker == row[0]:
                        already_holding = True
                    line_count += 1
            
        if already_holding == False:
            stocks_to_buy.append(current_ticker)
    
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



