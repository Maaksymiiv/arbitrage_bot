import json
import aiohttp, asyncio

delete_list = ["AVAUSDT", "ALPHAUSDT", "ADSUSDT", "BABYDOGEUSDT", "BRISEUSDT", "SQUIDGROWUSDT", "MIRUSDT",
               "PTXUSDT", "GOALUSDT", "MOONUSDT", "XEMUSDT", "VELOUSDT"]

async def get_bitmart_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api-cloud.bitmart.com/spot/v1/ticker"

        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()

            all_tickers = data.get('data').get('tickers')
            result = []
            for item in all_tickers:
                symbol = item.get("symbol").replace("_", "")
                if "USDT" in symbol:
                    ask_price = item.get("best_ask")
                    bid_price = item.get("best_bid")
                    volume = float(item.get("quote_volume_24h"))
                    link = item.get("url")
                    if symbol not in delete_list and volume > 30000:
                        result.append(
                            {
                                "symbol": symbol,
                                "ask_price": ask_price,
                                "bid_price": bid_price,
                                "volume": volume,
                                "link": link
                            }
                        )
            with open(r"data\bitmart_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\bitmart_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_bitmart_prices()

if __name__ == "__main__":
    asyncio.run(main())