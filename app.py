from hashlib import new
from os import close, getpgid, replace
from binance.client import Client
import math
from binance.enums import *
import random


apiKey = 'LLL'
apiSecret = 'lllL   '
long = ['BUY', 'LONG','buy','long']
short = ['SELL', 'SHORT','sell','short']

client = Client(apiKey , apiSecret)
print('Connected !')

def getAllTickers():
    x = client.get_all_tickers()
    return x

def symbolHandler(Input):
    for i in Input:
        if i == '-':
            out = Input.replace('-' , '')
        elif i == '/':
            out = Input.replace('/','')
        
        else:
            out = Input
    
    return out

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
        quantity=qtity
        )

    return x

def openShortPos(symbol, qtity):
    x = client.order_market_sell(
        symbol = symbol,
        quantity = qtity
        )

    return x

def getPosition(position):
    if position in long:
        position = SIDE_BUY
    elif position in short:
        position = SIDE_SELL
    else:
        position = O
    
    return position
Id = 'ZOEIJZDN2323947Y32UIENJKd'

def closeOrder(symbol, ID):
    #x = client.cancel_orders(
       # symbol = symbol,
       # orderId = ID
    #)
    
    #return x
    
    X = {'symbol' : symbol,
         'orderId' : ID
    }

    return X

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
        price=price
        )

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
    #risk and target for the trade checking.
    currPrice = getCurrentPrice(symbol)

    _risk = input('at how much is your percentage of risk ? : ')
    _target = input('at how much is your percentage of target ? : ')
    #Set up the tp and sl levels
    tpIfLong = setTakeProfitLevel(symbol , 'LONG', _target)
    tpIfShort = setTakeProfitLevel(symbol, 'SHORT', _target)
    slIfLong = setStopLossLevel(symbol , 'LONG', _risk)
    slIfShort = setStopLossLevel(symbol , 'SHORT', _risk)
    tp , sl = 0 , 0
    
    #checking position Input: 

    position = getPosition(position)

    if position == SIDE_BUY:
        tp , sl = tpIfLong , slIfLong
    
    elif position == SIDE_SELL:
        tp , sl = tpIfShort , slIfShort

    posDetails  = {'currPrice' : currPrice,
                        'Position' : position,
                        'takeProfit': tp,
                        'stopLoss' : sl,
                        'target' : _target,
                        'risk' : _risk
                        }
    
    print(posDetails)
    
    #Starting the actual trade
    #tradeStatus is a boolean
    almostTp1 = tp*(1 - 3/100)
    almostTp2 = tp*(1 + 3/100)
    almostSl1 = sl*(1 - 3/100)
    almostSl2 = sl*(1 + 3/100)
    L = [almostTp1, almostTp2 , almostSl1 , almostSl2]
    print(L)
    tradeStatus = True
    while tradeStatus:
        if position=='BUY':
            if almostTp1 < currPrice < almostTp2 or almostSl1 < currPrice < almostSl2:
                closeOrder(symbol, Id)
                print(closeOrder(symbol , Id))
        elif position=='SELL':
            print("0")
            break



def main():
    a = openTrade('LTCUSDT', 'SHORT')
    print(a)

main()