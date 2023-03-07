import json
import requests

binance_huobi_list = ["MDXUSDT"]
huobi_kucoin_list = ["HTRUSDT" ,"SOULUSDT", "VISIONUSDT", "DYPUSDT", "ABBCUSDT"]
binance_mexc = ["GMTUSDT", "MDXUSDT"]
kucoin_gate = ["FRMUSDT", "DYPUSDT", "SWPUSDT"]

def toFixed(num, digits=0):
    return f"{num:.{digits}f}"

def get_arbitrage(first_data, twice_data, firstex, twicex):
    firstex_symbols = []
    firstex_ask_prices = {}
    firstex_bid_prices = {}
    twicex_symbols = []
    twicex_ask_prices = {}
    twicex_bid_prices = {}
    firstex_volumes = {}
    twicex_volumes = {}
    firstex_links = {}
    twicex_links = {}

    for item in first_data:
        firstex_symbols.append(item.get('symbol'))
        firstex_ask_prices.update({firstex + "_ask_" + item.get('symbol'): item.get('ask_price')})
        firstex_bid_prices.update({firstex + "_bid_" + item.get('symbol'): item.get('bid_price')})
        firstex_volumes.update({firstex + "_" + item.get("symbol") + "vol": item.get("volume")})
        firstex_links.update({firstex+"_"+item.get('symbol')+"_link": item.get("link")})
    for item in twice_data:
        twicex_symbols.append(item.get('symbol'))
        twicex_ask_prices.update({twicex + "_ask_" + item.get('symbol'): item.get('ask_price')})
        twicex_bid_prices.update({twicex + "_bid_" + item.get('symbol'): item.get('bid_price')})
        twicex_volumes.update({twicex + "_" + item.get("symbol") + "vol": item.get("volume")})
        twicex_links.update({twicex+"_"+item.get('symbol')+"_link": item.get("link")})
    result = []

    with open(r'data\liq.txt', "r", encoding='utf-8') as file:
        min_liq = int(file.read())
    with open(r'data\spr.txt', "r", encoding='utf-8') as file:
        min_spr = float(file.read())

    for firstex_symbol in firstex_symbols:
        for twicex_symbol in twicex_symbols:
            try:
                if ((firstex == "Binance" and twicex == "Huobi" and twicex_symbol in binance_huobi_list) or
                (firstex == "Kucoin" and twicex == "Huobi" and twicex_symbol in huobi_kucoin_list) or
                (firstex == "Binance" and twicex == "Mexc" and twicex_symbol in binance_mexc) or
                (firstex == "Kucoin" and twicex == "GateIo" and twicex_symbol in kucoin_gate)):
                    continue
                elif firstex_symbol == twicex_symbol:
                    firstex_ask_price = float(firstex_ask_prices.get(firstex + "_ask_" + firstex_symbol))
                    firstex_bid_price = float(firstex_bid_prices.get(firstex + "_bid_" + firstex_symbol))
                    twicex_ask_price = float(twicex_ask_prices.get(twicex + "_ask_" + twicex_symbol))
                    twicex_bid_price = float(twicex_bid_prices.get(twicex + "_bid_" + twicex_symbol))
                    firstex_link = firstex_links.get(firstex + "_" + firstex_symbol + "_link")
                    twicex_link = twicex_links.get(twicex + "_" + twicex_symbol + "_link")
                    if firstex_ask_price < twicex_bid_price:

                        firstex_spred = twicex_bid_price / firstex_ask_price * 100 - 100
                        min_spred = min_spr
                        if firstex_spred > min_spred:
                            firstex_order_book = get_order_book(firstex, firstex_symbol, "ask", twicex_bid_price)
                            twicex_order_book = get_order_book(twicex, twicex_symbol, "bid", firstex_ask_price)
                            if float(firstex_order_book) > min_liq and float(twicex_order_book) > min_liq:
                                result.append(
                                    {
                                        "ex1": firstex,
                                        "ex2": twicex,
                                        "symbol": firstex_symbol,
                                        firstex + "_price": firstex_ask_price,
                                        twicex + "_price": twicex_bid_price,
                                        firstex + "_volume": toFixed(float(firstex_volumes.get(
                                            firstex + "_" + firstex_symbol + "vol"))),
                                        twicex + "_volume": toFixed(float(twicex_volumes.get(twicex + "_" + twicex_symbol + "vol"))),
                                        firstex + "_link": firstex_link,
                                        twicex + "_link": twicex_link,
                                        firstex + "_order_book": toFixed(firstex_order_book, 2),
                                        twicex + "_order_book": toFixed(twicex_order_book, 2),
                                        "spred": toFixed(firstex_spred, 4)
                                    }
                                )
                    elif twicex_ask_price < firstex_bid_price:
                        twicex_spred = firstex_bid_price / twicex_ask_price * 100 - 100
                        if twicex_spred > min_spred:
                            firstex_order_book = get_order_book(firstex, firstex_symbol, "bid", twicex_ask_price)
                            twicex_order_book = get_order_book(twicex, twicex_symbol, "ask", firstex_bid_price)
                            if float(firstex_order_book) > min_liq and float(twicex_order_book) > min_liq:
                                result.append(
                                    {
                                        "ex1": twicex,
                                        "ex2": firstex,
                                        "symbol": twicex_symbol,
                                        firstex + "_price": firstex_bid_price,
                                        twicex + "_price": twicex_ask_price,
                                        firstex + "_volume": toFixed(float(firstex_volumes.get(firstex + "_" + firstex_symbol + "vol"))),
                                        twicex + "_volume": toFixed(float(twicex_volumes.get(twicex + "_" + twicex_symbol + "vol"))),
                                        firstex + "_link": firstex_link,
                                        twicex + "_link": twicex_link,
                                        firstex + "_order_book": toFixed(firstex_order_book, 2),
                                        twicex + "_order_book": toFixed(twicex_order_book, 2),
                                        "spred": toFixed(float(twicex_spred), 4)
                                    }
                                )
            except:
                continue

    with open(r"D:\python\Arbitrage_Bot\data\spred.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

def get_order_book(ex, symbol, order, limit_price):
    symbol = symbol[0:-4]
    quote = symbol[-4:]
#BINANCE
    if ex == "Binance":
        url = f"https://api.binance.com/api/v3/depth?symbol={symbol}USDT"
        response = requests.get(url=url)
        data = response.json()
        sum = 0
        if order == "bid":
            bids = data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price
#KUCOIN
    elif ex == "Kucoin":
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol={symbol}-USDT"
        response = requests.get(url=url)
        data = response.json()
        orders = data.get('data')
        sum = 0
        if order == "bid":
            bids = orders.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = orders.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price
#HUOBI
    elif ex == "Huobi":
        url = f"https://api.huobi.pro/market/depth?symbol={symbol.lower()}usdt&type=step0"
        response = requests.get(url=url)
        data = response.json()
        orders = data.get('tick')
        sum = 0
        if order == "bid":
            bids = orders.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = orders.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price
#OKX
    elif ex == "OKX":
        url = f"https://www.okx.com/api/v5/market/books-lite?instId={symbol}-USDT"
        response = requests.get(url=url)
        data = response.json()
        orders = data.get('data')
        sum = 0
        for items in orders:
            if order == "bid":
                bids = items.get('bids')
                for item in bids:
                    if float(item[0]) > limit_price:
                        sum += float(item[1])
            elif order == "ask":
                asks = items.get('asks')
                for item in asks:
                    if float(item[0]) < limit_price:
                        sum += float(item[1])
        return sum * limit_price
#MEXC
    elif ex == "Mexc":
        url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}USDT"
        response = requests.get(url=url)
        data = response.json()
        sum = 0
        if order == "bid":
            bids = data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price
#GateIO
    elif ex == "GateIo":
        url = f"https://api.gateio.ws/api/v4/spot/order_book?currency_pair={symbol}_USDT&limit=100"
        response = requests.get(url=url)
        data = response.json()
        sum = 0
        if order == "bid":
            bids = data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price
#BITFINEX
    elif ex == "Bitfinex":
        url = f"https://api-pub.bitfinex.com/v2/book/t{symbol}USD/P0?len=25"
        response = requests.get(url=url)
        data = response.json()
        sum = 0
        for item in data:
            if order == "bid" and float(item[2]) > 0 and float(item[0]) > limit_price:
                sum += float(item[2])
            elif order == "ask" and float(item[2]) < 0 and float(item[0]) < limit_price:
                sum += float(item[2])
        return abs(sum) * limit_price

#BITMART
    elif ex == "Bitmart":
        url = f"https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol={symbol}_USDT"
        response = requests.get(url=url)
        all_data = response.json()
        data = all_data.get('data')
        sum = 0
        if order == "bid":
            bids = data.get("buys")
            for item in bids:
                if float(item.get('price')) > limit_price:
                    sum += float(item.get('amount'))
        elif order == "ask":
            asks = data.get("sells")
            for item in asks:
                if float(item.get('price')) < limit_price:
                    sum += float(item.get('amount'))
        return sum * limit_price

#WHITEBIT
    elif ex == "WhiteBit":
        url = f"https://whitebit.com/api/v1/public/depth/result?market={symbol}_USDT"
        response = requests.get(url=url)
        data = response.json()
        sum = 0
        if order == "bid":
            bids = data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return sum * limit_price

#BITGET
    elif ex == "Bitget":
        url = f"https://api.bitget.com/api/spot/v1/market/depth?symbol={symbol}USDT_SPBL"
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        data = all_data.get('data')
        if order == "bid":
            bids = data.get("bids")
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get("asks")
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price

#LBANK
    elif ex == "Lbank":
        url = f"https://api.lbkex.com/v1/depth.do?symbol={symbol.lower()}_usdt&size=60"
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        if order == "bid":
            bids = all_data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        if order == "ask":
            asks = all_data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price
#BKEX
    elif ex == "BKEX":
        url = f"https://api.bkex.com/v2/q/depth?symbol={symbol}_USDT"
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        data = all_data.get('data')
        if order == "bid":
            bids = data.get("bid")
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get("ask")
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price

#BTCEX
    elif ex == 'BTCEX':
        url = f'https://api.btcex.com/api/v1/public/get_order_book?instrument_name={symbol}-USDT-SPOT'
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        data = all_data.get('result')
        if order == "bid":
            bids = data.get("bids")
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get("asks")
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price
#XTCOM
    elif ex == "XT":
        url = f'https://sapi.xt.com/v4/public/depth?symbol={symbol.lower()}_usdt'
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        data = all_data.get('result')
        if order == "bid":
            bids = data.get("bids")
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get("asks")
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price
#COINEX
    elif ex == "CoinEx":
        url = f'https://api.coinex.com/v1/market/depth?market={symbol.lower()}usdt&limit=50&merge=0'
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        data = all_data.get('data')
        if order == "bid":
            bids = data.get("bids")
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        elif order == "ask":
            asks = data.get("asks")
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price

#Bitrue
    elif ex == "Bitrue":
        url = f'https://www.bitrue.com/api/v1/depth?symbol={symbol.lower()}usdt'
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        if order == "bid":
            bids = all_data.get('bids')
            for item in bids:
                if float(item[0]) > limit_price:
                    sum += float(item[1])
        if order == "ask":
            asks = all_data.get('asks')
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price
    else:
        return "-"

def main():
     with open(r"D:\python\Arbitrage_Bot\data\binance_price.json", "r", encoding="utf-8") as file:
         binance_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\kucoin_price.json", "r", encoding="utf-8") as file:
         kucoin_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\bybit_price.json", "r", encoding="utf-8") as file:
         bybit_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\huobi_price.json", "r", encoding="utf-8") as file:
         huobi_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\okx_price.json", "r", encoding="utf-8") as file:
         okx_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\mexc_price.json", "r", encoding="utf-8") as file:
         mexc_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\gateio_price.json", "r", encoding="utf-8") as file:
         gateio_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\bitmart_price.json", "r", encoding="utf-8") as file:
         bitmart_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\whitebit_price.json", "r", encoding="utf-8") as file:
         whitebit_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\bitget_price.json", "r", encoding="utf-8") as file:
         bitget_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\lbank_price.json", "r", encoding="utf-8") as file:
         lbank_data = json.load(file)
     with open(r"D:\python\Arbitrage_Bot\data\xtcom.price.json", "r", encoding="utf-8") as file:
         xt_data = json.load(file)

     get_arbitrage(gateio_data, xt_data, "GateIo", "XT")

if __name__ == '__main__':
    main()