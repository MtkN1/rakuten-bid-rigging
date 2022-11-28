import asyncio

from rich.pretty import pprint

from libs.wrapper import RakutenApi

BASE_URL = "https://exchange.rakuten-wallet.co.jp"


async def main():
    async with RakutenApi() as rakuten:
        # r = await client.get("/api/v1/cfd/symbol")
        # r = await client.get("/api/v1/cfd/equitydata")
        # r = await client.get("/api/v1/cfd/order", params={"symbolId": 8})
        # r = await client.delete(
        #     "/api/v1/cfd/order", params={"symbolId": 8, "id": 49024411}
        # )

        # data = {
        #     "symbolId": 8,
        #     "orderPattern": "NORMAL",
        #     "orderData": {
        #         "orderBehavior": "OPEN",
        #         "orderSide": "BUY",
        #         "orderType": "LIMIT",
        #         "price": "152161",
        #         "amount": "0.2",
        #         "orderExpire": "GTC",
        #         "closeBehavior": "FIFO",
        #         "postOnly": True,
        #     },
        # }
        # r = await client.post("/api/v1/cfd/order", json=data)

        # data = {
        #     "symbolId": 8,
        #     "orderPattern": "NORMAL",
        #     "orderData": {
        #         "orderId": 49084365,
        #         "orderType": "LIMIT",
        #         "price": "152160",
        #         "amount": "0.1",
        #     },
        # }
        # r = await client.put("/api/v1/cfd/order", json=data)

        # r = await client.get_equitydata()
        # resps = await asyncio.gather(
        #     rakuten.get_equitydata(),
        #     rakuten.get_asset(),
        #     rakuten.get_order(symbol_id=7),
        #     rakuten.get_position(symbol_id=7),
        # )
        # for r in resps:
        #     pprint(r.json(), indent_guides=False)

        r = await rakuten.get_symbol()
        for x in r.data:
            x

        pprint(r.data)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
