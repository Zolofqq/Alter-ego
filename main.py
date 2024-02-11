from binance.um_futures import UMFutures
from keys import key, secret, TELEGRAM_CHANNEL, TELEGRAM_TOKEN
import time
import requests

TP = 1.40
SL = 1.00
DEPOSIT = 10

client = UMFutures(key=key, secret=secret)

def send_message(text):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    data = {
        'chat_id': TELEGRAM_CHANNEL,
        'text': text
    }
    response = requests.post(url, data=data)
    
def get_top_coin():
    data = client.ticker_24hr_price_change()
    change = {}
    for i in data:
        change[i['symbol']] = float(i['priceChangePercent'])
        
    coin = max(change, key=change.get)
    print(f"Top coin is: {coin}: {change[coin]}")
    send_message(f"Top coin is: {coin}: {change[coin]}")
    return coin

def get_symbol_price(symbol):
    price = round(float(client.ticker_price(symbol)['price']), 5)
    print(f"Price: {price}")
    send_message(f"Price: {price}")
    return price

def get_trade_volume():
    volume = DEPOSIT
    print(f"Trade volume: {volume}")
    return volume

def open_long_market_order(symbol, volume):
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': volume,
    }
    
    response = client.new_order(**params)
    print(response)
    
def open_short_market_order(symbol, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': volume,
    }
    
    response = client.new_order(**params)
    print(response)
    
def open_stop_order(symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'STOP_MARKET',
        # 'timeInForce': 'GTC', 
        'stopPrice': price,
        'quantity': volume,
    }
    response = client.new_order(**params) 
    print(response)
    
def open_take_profit_order (symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'TAKE_PROFIT_MARKET',
        # 'timeInForce': 'GTC',
        'stopPrice': price,
        'quantity': volume,
    }
    response = client.new_order(**params) 
    print(response)
    
def get_stop_loss_price_long():
    stop_loss_price_long = round(price - (price * SL), 4)
    print(f"Stop Loss: {stop_loss_price_long}")
    return stop_loss_price_long

def get_take_profit_price_long():
    take_profit_price_long = round((price + TP + price), 4)
    print(f"Take Profit: {take_profit_price_long}")
    return take_profit_price_long

def get_stop_loss_price_short():
    stop_loss_price_short = round(price - (price * TP), 4)
    print(f"Stop Loss: {stop_loss_price_short}")
    return stop_loss_price_short

def get_take_profit_price_short():
    take_profit_price_short = round((price + SL + price), 4)
    print(f"Take Profit: {take_profit_price_short}")
    return take_profit_price_short

symbol = 'ORDIUSDT'
open_position = False

while True:
    if open_position == False:
        print("Posisition inactive")
        send_message("Posisition inactive")
        volume = DEPOSIT
        price = get_symbol_price(symbol)
        open_long_market_order(symbol, volume)
        open_short_market_order(symbol, volume)
        send_message("The was open")
        time.sleep(2)
        take_profit_price_long = get_take_profit_price_long()
        stop_loss_price_long = get_stop_loss_price_long()
        take_profit_price_short = get_take_profit_price_short()
        stop_loss_price_short = get_stop_loss_price_short()
        open_stop_order(symbol, take_profit_price_long, volume)
        open_stop_order(symbol, take_profit_price_short, volume)
        send_message("The was open Stop order")
        time.sleep(2)
        open_take_profit_order(symbol, take_profit_price_long, volume)
        open_take_profit_order(symbol, take_profit_price_short, volume)
        send_message("The was open Take Profit order")
        open_position = True
        break
    
    else:
        print("Positions active")
        send_message("Positions active")
        time.sleep(30)