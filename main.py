from binance.client import Client
import math
from binance.enums import *
import random

def sep():
    print('-------------------------------------------------------------------------------------------------------------------------------------------------------')

   
apiKey = input('Api key : ')
sep()
apiSecret = input('Api secret : ')

long , short = ['BUY', 'LONG','buy','long'], ['SELL', 'SHORT','sell','short']
print(long , short)

try:
    client = Client(apiKey , apiSecret)
    print('Connected !')
except Exception:
    print('Authentication error')

def getAllTickers():
    x = client.get_all_tickers()
    return x

def symbolHandler(Input):
    for i in Input:
        if i == '-':
            x = Input.replace('-' ,'')
        elif i == '/':
            x = Input.replace('/','')
        else:
            x = Input

    return x

def getCurrentPrice(symbol):
    index = getAllTickers()

    for i in index:
        find = i
        if find['symbol'] == symbol:
            out = find['price']
            return out
    
    return False

def openLongPos(symbol, qtity):
    x = client.order_market_buy(
        symbol=symbol,
        quantity=qtity)

    return x

def openShortPos(symbol, qtity):
    x = client.order_market_sell(
        symbol = symbol,
        quantity = qtity)
    
    return x

def getPosition(position):
    if position in long:
        position = SIDE_BUY
    elif position in short:
        position = SIDE_SELL
    else:
        position = 0
    
    return position

def closeOrder(symbol, ID):
    x = client.cancel_orders(
        symbol = symbol,
        orderId = ID)
    
    return x
    
def openSpecificBuyLimit(symbol, qtity, price):
    x = client.order_limit_buy(
    symbol=symbol,
    quantity=qtity,
    price=price)

    return x

def openSpecificSellLimit(symbol, qtity, price):
    x = client.order_limit_sell(
        symbol=symbol,
        quantity=qtity,
        price=price)

    return x

def setStopLossLevel(symbol, position , risking): #symb: BTCUSDT , #position: 'LONG' , risking: "10%"
    currentPrice = getCurrentPrice(symbol)
    currentPrice = float(currentPrice)
    p = str(risking[-1])
    if p == "%":    
        risking = risking[0: len(risking)-1]
        risking = float(risking) / 100
    else:
        try:
            risking = float(risking)
            risking = risking / 100
        except Exception:
            print('Wrong input')

    if position == 'LONG':
        currentPrice *= (1 - risking) 
    elif position == 'SHORT':
        currentPrice *= (1 + risking)
    
    x = currentPrice

    return x

def setTakeProfitLevel(symbol, position, target):
    currentPrice = getCurrentPrice(symbol)
    currentPrice = float(currentPrice)
    p = str(target[-1])
    if p == "%":    
        target = target[0: len(target)-1]
        target = float(target) / 100
    else:
        try:
            target = float(target)
            target = target / 100
        except Exception:
            print('Wrong input')

    if position == 'LONG':
        currentPrice *= (1 + target) 
    elif position == 'SHORT':
        currentPrice *= (1 - target)
    
    x = currentPrice

    return x

def openTrade(symbol , position):
    quant = int(input('Quantity you wanna short or buy :'))
    currPrice = getCurrentPrice(symbol)
    _risk = input('at how much is your percentage of risk ? : ')
    _target = input('at how much is your percentage of target ? : ')
    #Set up the tp and sl levels
    tpIfLong = setTakeProfitLevel(symbol , 'LONG', _target)
    tpIfShort = setTakeProfitLevel(symbol, 'SHORT', _target)
    slIfLong = setStopLossLevel(symbol , 'LONG', _risk)
    slIfShort = setStopLossLevel(symbol , 'SHORT', _risk)
    takeProfit , stopLoss = 0 , 0
    
    #checking position Input: 
    #Long >> 'LONG'>> 'BUY'
    #Short >> 'SHORT' >> 'SELL'
    position = getPosition(position)

    if position == SIDE_BUY:
        takeProfit , stopLoss = tpIfLong , slIfLong
    
    elif position == SIDE_SELL:
        takeProfit , stopLoss = tpIfShort , slIfShort
        
    currPrice = getCurrentPrice(symbol)
    positionDetails  = {
                        'currPrice' : currPrice,
                        'Position' : position,
                        'takeProfit': takeProfit,
                        'stopLoss' : stopLoss,
                        'target' : _target,
                        'risk' : _risk
                        }

    print(positionDetails)
    
    n = int(input("Margin of error (in hundredths): "))
    n /=100
    
    if position == 'BUY':
        currPrice = getCurrentPrice(symbol)
        openLongPos(symbol , quant)
        id = openLongPos(symbol, quant)
        id = id['orderId']
        while True:
            currPrice = getCurrentPrice(symbol)
            if takeProfit-n <= currPrice or currPrice <= stopLoss+n:
                closeOrder(symbol, id)
                print(closeOrder(symbol , id))
                break

    elif position == 'SELL':
        currPrice = getCurrentPrice(symbol)
        openShortPos(symbol, quant)
        id = openShortPos(symbol, quant)
        id = id['orderId']
        while True:
            currPrice = getCurrentPrice(symbol)
            if currPrice <= takeProfit+n or currPrice >= stopLoss-n:
                closeOrder(symbol, id)
                print(closeOrder(symbol, id))
                break
        
    sumUp = client.get_order(
                symbol=symbol,
                orderId=id)

    return sumUp


def main():
    print("Hello welcome to trading world !")
    method = int(input('choose your method : '))
    sep()
    match method:
        case 1:
            print('GET CURRENT PRICE SELECTED')
            Symbol = input('Symbol : ')
            x = getCurrentPrice(Symbol)
            print(x)

        case 2:
            print('OPEN LONG POSITION SELECTED !')
            sep()
            Symbol = input('Symbol')
            sep()
            Quantity = int(input('Quantity : '))
            x = openLongPos(Symbol, Quantity)
            print(x)

        case 3:
            print('OPEN SHORT POSITION SELECTED !')
            sep()
            Symbol = input('Symbol : ')
            sep()
            Quantity = int(input('Quantity : '))
            x = openShortPos(Symbol , Quantity)
            print(x)

        case 4:
            print('CLOSE ORDER SELECTED !')
            sep()
            Symbol = input('Symbol: ')
            sep()
            Id = input('OrderId :')
            x = closeOrder(Symbol , Id)
            print(x)

        case 5:
            print('BUY LIMIT SELECTED ! : ')
            sep()
            Symbol = input('Symbol : ')
            sep()
            Quantity = int(input('Quantity : '))
            sep()
            Price = input('Price')
            x = openSpecificBuyLimit(Symbol, Quantity, Price)
            print(x)

        case 6:
            print('SELL LIMIT SELECTED !: )
            sep()
            Symbol = input('Symbol : ')
            sep()
            Quantity = int(input('Quantity : '))
            sep()
            Price = input('Price')
            x = openSpecificSellLimit(Symbol, Quantity, Price)
            print(x)

        case 7:
            print('OPEN TRADE SELECTED !')
            Symbol = input('Symbol : ')
            sep()
            Position = input('Position : ')
            x = openTrade(Symbol, Position)
            print(x)
        
main()
