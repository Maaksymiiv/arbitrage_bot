import json
import aiohttp, asyncio

delete_list = ["BETHUSDT", "BABYDOGEUSDT", "KISHUUSDT", "GFTUSDT", "TRADEUSDT", "VELOUSDT"]  #01.03

async def get_okx_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://www.okx.com/priapi/v5/market/tickers?instType=SPOT"

        response = await session.get(url=url)
        if response.status  == 200:
            data = await response.json()
            all_symbols = data.get('data')
            result = []
            for item in all_symbols:
                symbol = item.get('instId').replace("-", "")
                price = item.get('last')
                bid_price = item.get("bidPx")
                ask_price = item.get("askPx")
                vol = float(item.get('volCcy24h'))
                symbol_link = symbol[0:-4].lower()
                quote = symbol[-4:]
                link = f"https://www.okx.com/ua/trade-spot/{symbol_link}-{quote}"
                if vol > 30000 and symbol not in delete_list and "USDT" in symbol:
                    result.append(
                        {
                            "symbol": symbol,
                            "bid_price": bid_price,
                            "ask_price": ask_price,
                            "volume": vol,
                            "link": link
                        }
                    )
            with open(r"data\okx_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
        else:
            result = []
            result.append(
                {
                    "symbol": "-",
                    "ask_price": "-",
                    "bid_price": "-",
                    "volume": 0,
                    "link": "-"
                }
            )
            with open(r"data\okx_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_okx_prices()

if __name__ == '__main__':
    asyncio.run(main())