import asyncio
import contextlib

import httpx
from dotenv import dotenv_values
from rich.pretty import pprint

from libs.auth import RakutenAuth


def create_rakuten_client(dotenv_path: str | None = None) -> httpx.AsyncClient:
    base_url = "https://exchange.rakuten-wallet.co.jp"

    if dotenv_path is None:
        return httpx.AsyncClient(base_url=base_url)
    else:
        env = dotenv_values(dotenv_path)
        auth = RakutenAuth(env.get("RAKUTEN_API_KEY"), env.get("RAKUTEN_API_SECRET"))
        proxies = env.get("PROXY_URL", AssertionError("PROXY_URL does not exist"))
        return httpx.AsyncClient(auth=auth, proxies=proxies, base_url=base_url)


async def main():
    symbol_id = 7
    open_amount = "0.01"

    async with contextlib.AsyncExitStack() as stack:
        client_pub, client_a, client_b = [
            await stack.enter_async_context(create_rakuten_client(x))
            for x in (None, "ENV/a.env", "ENV/b.env")
        ]

        pprint("Start logic")
        while True:
            pprint("Start order sequence")

            try:
                # Equity
                before_equity = {}

                r = await client_a.get("/api/v1/cfd/equitydata")
                r.raise_for_status()
                before_equity["a"] = r.json()

                r = await client_b.get("/api/v1/cfd/equitydata")
                r.raise_for_status()
                before_equity["b"] = r.json()

                pprint(format(" before_equity ", "=^80"))
                pprint(before_equity)

                await asyncio.sleep(1.0)

                # Position
                before_position = {}

                r = await client_a.get(
                    "/api/v1/cfd/position",
                    params={
                        "symbolId": symbol_id,
                    },
                )
                r.raise_for_status()
                before_position["a"] = r.json()

                r = await client_b.get(
                    "/api/v1/cfd/position",
                    params={
                        "symbolId": symbol_id,
                    },
                )
                r.raise_for_status()
                before_position["b"] = r.json()

                pprint(format(" before_position ", "=^80"))
                pprint(before_position)

                await asyncio.sleep(1.0)

                if not len(before_position["b"]) and not len(before_position["a"]):
                    # Orderbook
                    r = await client_pub.get(
                        "/api/v1/orderbook",
                        params={
                            "symbolId": symbol_id,
                        },
                    )
                    r.raise_for_status()
                    orderbook = r.json()

                    mid_price = orderbook["midPrice"]

                    # Open order
                    open_order = {}

                    r = await client_b.post(
                        "/api/v1/cfd/order",
                        json={
                            "symbolId": symbol_id,
                            "orderPattern": "NORMAL",
                            "orderData": {
                                "orderBehavior": "OPEN",
                                "orderSide": "BUY",
                                "orderType": "LIMIT",
                                "price": mid_price,
                                "amount": open_amount,
                                "orderExpire": "GTC",
                                "closeBehavior": "FIFO",
                                "postOnly": True,
                            },
                        },
                    )
                    r.raise_for_status()
                    open_order["b"] = r.json()

                    r = await client_a.post(
                        "/api/v1/cfd/order",
                        json={
                            "symbolId": symbol_id,
                            "orderPattern": "NORMAL",
                            "orderData": {
                                "orderBehavior": "OPEN",
                                "orderSide": "SELL",
                                "orderType": "MARKET",
                                "amount": open_amount,
                                "orderExpire": "GTC",
                                "closeBehavior": "FIFO",
                            },
                        },
                    )
                    r.raise_for_status()
                    open_order["a"] = r.json()

                    pprint(format(" open_order ", "=^80"))
                    pprint(open_order)

                    await asyncio.sleep(1.0)

                elif len(before_position["b"]) and len(before_position["a"]):
                    # Orderbook
                    r = await client_pub.get(
                        "/api/v1/orderbook",
                        params={
                            "symbolId": symbol_id,
                        },
                    )
                    r.raise_for_status()
                    orderbook = r.json()

                    mid_price = orderbook["midPrice"]

                    # Close order
                    close_order = {}

                    r = await client_b.post(
                        "/api/v1/cfd/order",
                        json={
                            "symbolId": symbol_id,
                            "orderPattern": "NORMAL",
                            "orderData": {
                                "orderBehavior": "CLOSE",
                                "positionId": before_position["b"][0]["id"],
                                "orderSide": "SELL",
                                "orderType": "LIMIT",
                                "price": mid_price,
                                "amount": open_amount,
                                "orderExpire": "GTC",
                                "postOnly": True,
                            },
                        },
                    )
                    r.raise_for_status()
                    close_order["b"] = r.json()

                    r = await client_a.post(
                        "/api/v1/cfd/order",
                        json={
                            "symbolId": symbol_id,
                            "orderPattern": "NORMAL",
                            "orderData": {
                                "orderBehavior": "CLOSE",
                                "positionId": before_position["a"][0]["id"],
                                "orderSide": "BUY",
                                "orderType": "MARKET",
                                "amount": open_amount,
                                "orderExpire": "GTC",
                            },
                        },
                    )
                    r.raise_for_status()
                    close_order["a"] = r.json()

                    pprint(format(" close_order ", "=^80"))
                    pprint(close_order)

                    await asyncio.sleep(1.0)

                # Equity
                after_equity = {}

                r = await client_a.get("/api/v1/cfd/equitydata")
                r.raise_for_status()
                after_equity["a"] = r.json()

                r = await client_b.get("/api/v1/cfd/equitydata")
                r.raise_for_status()
                after_equity["b"] = r.json()

                pprint(format(" after_equity ", "=^80"))
                pprint(after_equity)

                await asyncio.sleep(1.0)

                # Position
                after_position = {}

                r = await client_a.get(
                    "/api/v1/cfd/position",
                    params={
                        "symbolId": symbol_id,
                    },
                )
                r.raise_for_status()
                after_position["a"] = r.json()

                r = await client_b.get(
                    "/api/v1/cfd/position",
                    params={
                        "symbolId": symbol_id,
                    },
                )
                r.raise_for_status()
                after_position["b"] = r.json()

                pprint(format(" after_position ", "=^80"))
                pprint(after_position)

            except httpx.HTTPStatusError as e:
                pprint(format(" httpx.HTTPStatusError ", "=^80"))
                pprint(e)
                pprint(e.request)
                pprint(e.request.content)
                pprint(e.response)
                pprint(e.response.text)

            pprint("Wait for next loop ...")

            try:
                await asyncio.sleep(30.0)
            except asyncio.CancelledError:
                return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
