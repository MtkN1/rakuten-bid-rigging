import httpx
import pytest
from dotenv import dotenv_values
from rich.pretty import pprint

from src.libs.auth import RakutenAuth


@pytest.fixture
def env() -> dict[str, str | None]:
    return dotenv_values("ENV/b.env")


@pytest.fixture
def auth(env: dict[str, str | None]):
    return RakutenAuth(env.get("RAKUTEN_API_KEY"), env.get("RAKUTEN_API_SECRET"))


@pytest.fixture
def client(auth: auth):
    return httpx.Client(auth=auth, base_url="https://exchange.rakuten-wallet.co.jp")


def test_equitydata(client: httpx.Client):
    r = client.get("/api/v1/cfd/equitydata")

    assert r.is_success

    content = r.json()

    assert "code" not in content

    pprint(content)


def test_position(client: httpx.Client):
    r = client.get("/api/v1/cfd/position?symbolId=17")

    content = r.json()
    pprint(content)

    assert "code" not in content


def test_open_buy_order(client: httpx.Client):
    r = client.post(
        "/api/v1/cfd/order",
        json={
            "symbolId": 7,
            "orderPattern": "NORMAL",
            "orderData": {
                "orderBehavior": "OPEN",
                "orderSide": "BUY",
                "orderType": "MARKET",
                "amount": "0.01",
                "orderExpire": "GTC",
                "closeBehavior": "FIFO",
            },
        },
    )

    content = r.json()
    pprint(content)

    assert "code" not in content


def test_open_sell_order(client: httpx.Client):
    r = client.post(
        "/api/v1/cfd/order",
        json={
            "symbolId": 7,
            "orderPattern": "NORMAL",
            "orderData": {
                "orderBehavior": "OPEN",
                "orderSide": "SELL",
                "orderType": "MARKET",
                "amount": "0.01",
                "orderExpire": "GTC",
                "closeBehavior": "FIFO",
            },
        },
    )

    content = r.json()
    pprint(content)

    assert "code" not in content


def test_close_order(client: httpx.Client):
    r = client.post(
        "/api/v1/cfd/order",
        json={
            "symbolId": 17,
            "orderPattern": "NORMAL",
            "orderData": {
                "orderBehavior": "CLOSE",
                "positionId": 20111,
                "orderSide": "SELL",
                "orderType": "LIMIT",
                "amount": "100",
                "price": "128.56",
                # "orderExpire": "GTC",
                # "closeBehavior": "FIFO",
            },
        },
    )

    content = r.json()
    pprint(content)

    # assert "code" not in content


def test_close_all(client: httpx.Client):
    r = client.post(
        "/api/v1/cfd/order/close-all",
        json={
            "symbolId": 7,
        },
    )

    content = r.json()
    pprint(content)

    assert "code" not in content
