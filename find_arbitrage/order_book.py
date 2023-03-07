import requests

def get_order_book(ex, symbol, order, limit_price):
    symbol = symbol[0:-4]
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

# BITGET
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
# LATOKEN
    elif ex == "Latoken":
        url = f"https://api.latoken.com/v2/book/{symbol}/USDT"
        response = requests.get(url=url)
        all_data = response.json()
        sum = 0
        if order == "bid":
            bids = all_data.get('bid')
            for item in bids:
                if float(item.get('price')) > limit_price:
                    sum += float(item.get('cost'))
        elif order == "ask":
            asks = all_data.get('ask')
            for item in asks:
                if float(item.get('price')) > limit_price:
                    sum += float(item.get('cost'))
        return float(sum)
#BKEX
    elif ex == "BKEX":
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
            print(asks)
            for item in asks:
                if float(item[0]) < limit_price:
                    sum += float(item[1])
        return float(sum) * limit_price
# BTCEX
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
# XTCOM
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

# COINEX
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
# Bitrue
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
   print(get_order_book("XT", "BTCUSDT", "bid", 21940))

if __name__ == "__main__":
    main()