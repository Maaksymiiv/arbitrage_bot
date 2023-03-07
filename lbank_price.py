import json
import aiohttp, asyncio

delete_list = ["BABYDOGEUSDT", "GMTUSDT", "VEXUSDT", "SAITAMAUSDT", "TRUUSDT", "FWCUSDT", "QUACKUSDT", "VOLTUSDT",
               "FLOKIUSDT", "KISHUUSDT", "ERNUSDT", "MONUSDT", "GFTUSDT", "RENUSDT", "BNTUSDT", "TUSDT", "CELRUSDT", "ANCUSDT",
               "LOOKSUSDT", "WINUSDT", "PONDUSDT", "AGIXUSDT", "AGLDUSDT", "TABOOUSDT", "FREEUSDT", "SHINJAUSDT",
               "RAREUSDT", "REDUSDT", "ESGUSDT", "BRISEUSDT", "XSPECTAR", "HALOUSDT"]

async def get_lbank_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.lbkex.com/v1/ticker.do?symbol=all"
        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()
            result = []
            for item in data:
                symbol = item.get('symbol')
                full_symbol = symbol.upper().replace("_", "")
                ticker = item.get('ticker')
                price = ticker.get('latest')
                vol = float(ticker.get('vol'))
                link = f"https://www.lbank.com/en-US/trade/{symbol}/"
                if vol > 30000 and "USDT" in full_symbol and "5" not in symbol and "5" not in symbol and full_symbol not in delete_list:
                    result.append(
                        {
                            "symbol": full_symbol,
                            "bid_price": price,
                            "ask_price": price,
                            "volume": vol,
                            "link": link
                        }
                    )
            with open(r"data\lbank_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\lbank_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_lbank_prices()

if __name__ == '__main__':
    asyncio.run(main())