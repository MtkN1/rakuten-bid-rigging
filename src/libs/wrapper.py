from collections.abc import Coroutine
from json import JSONDecodeError
from typing import Any, Self

import httpx
from dotenv import dotenv_values

from .auth import RakutenAuth
from .models import NoResponse, Response, SymbolResponse, TickerResponse


class ClientWapper:
    async def __aenter__(self: Self) -> Self:
        _client = getattr(self, "_client", None)
        if _client:
            setattr(self, "_client", await _client.__aenter__())

        return self

    async def __aexit__(self: Self, *args: tuple[Any, ...]) -> None:
        _client = getattr(self, "_client", None)
        if _client:
            await _client.__aexit__(*args)


class RakutenApi(ClientWapper):
    BASE_URL = "https://exchange.rakuten-wallet.co.jp"

    def __init__(self: Self) -> None:
        self._client = httpx.AsyncClient(base_url=self.BASE_URL)

        dotenv = dotenv_values()
        self._auth = RakutenAuth(
            dotenv.get("RAKUTEN_API_KEY", ""), dotenv.get("RAKUTEN_API_SECRET", "")
        )

    def _request(
        self: Self, method: str, path: str, parameters: Any, private: bool = False
    ):
        params = None
        json = None
        auth = None

        match method:
            case "GET" | "DELETE":
                params = parameters
            case "POST" | "PUT":
                json = parameters

        if private:
            auth = self._auth

        return self._client.request(
            method,
            path,
            params=params,
            json=json,
            auth=auth,
        )

    async def _request_wrapper(
        self: Self, method: str, path: str, parameters: Any, private: bool = False
    ) -> Response:
        r = await self._request(method, path, parameters, private)
        try:
            data = r.json()
        except JSONDecodeError:
            data = NoResponse()
        return Response(r.headers, data, r)

    def get_symbol(
        self: Self,
        authority: str | None = None,
    ) -> Coroutine[Any, Any, Response[SymbolResponse]]:
        return self._request_wrapper(
            method="GET",
            path="/api/v1/cfd/symbol",
            parameters={
                "authority": authority,
            },
        )

    def get_ticker(
        self: Self,
        symbol_id: int,
    ) -> Coroutine[Any, Any, Response[TickerResponse]]:
        return self._request_wrapper(
            method="GET",
            path="/api/v1/ticker",
            parameters={
                "symbolId": symbol_id,
            },
        )

    def get_asset(
        self: Self,
    ) -> Coroutine[Any, Any, httpx.Response]:
        return self._request(
            method="GET",
            path="/api/v1/asset",
            parameters=None,
            private=True,
        )

    def get_equitydata(
        self: Self,
    ) -> Coroutine[Any, Any, httpx.Response]:
        return self._request(
            method="GET",
            path="/api/v1/cfd/equitydata",
            parameters=None,
            private=True,
        )

    def get_order(
        self: Self,
        symbol_id: int,
    ) -> Coroutine[Any, Any, httpx.Response]:
        return self._request(
            method="GET",
            path="/api/v1/cfd/order",
            parameters={
                "symbolId": symbol_id,
            },
            private=True,
        )

    def get_position(
        self: Self,
        symbol_id: int,
    ) -> Coroutine[Any, Any, httpx.Response]:
        return self._request(
            method="GET",
            path="/api/v1/cfd/position",
            parameters={
                "symbolId": symbol_id,
            },
            private=True,
        )
