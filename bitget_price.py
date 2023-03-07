import json
import aiohttp, asyncio

delete_list = ["HUBUSDT", "BLURUSDT", "VELOUSDT"]

async def get_bitget_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.bitget.com/api/spot/v1/market/tickers"

        response = await session.get(url=url)
        if response.status == 200:
            all_data = await response.json()
            data = all_data.get('data')

            result = []
            for item in data:
                symbol = item.get('symbol')
                if "USDT" in symbol:
                    bid_price = item.get("buyOne")
                    ask_price = item.get("sellOne")
                    volume = float(item.get("quoteVol"))
                    link = f"https://www.bitget.com/en/spot/{symbol}_SPBL?type=spot"

                    if volume > 30000 and "USDT" in symbol and symbol not in delete_list:
                        result.append(
                            {
                                "symbol": symbol,
                                "bid_price": bid_price,
                                "ask_price": ask_price,
                                "volume": volume,
                                "link": link
                            }
                        )

            with open(r"data\bitget_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\bitget_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_bitget_prices()

if __name__ == '__main__':
    asyncio.run(main())
