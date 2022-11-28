from dataclasses import dataclass
from typing import Generic, TypeAlias, TypedDict, TypeVar

import httpx
from httpx._types import HeaderTypes

T = TypeVar("T")


class NoResponse:
    """
    No response content
    """


@dataclass
class Response(Generic[T]):
    headers: HeaderTypes
    data: T  # | NoResponse
    _raw: httpx.Response


SymbolObject: TypeAlias = TypedDict(
    "SymbolObject",
    {
        "id": int,
        "authority": str,
        "tradeType": str,
        "currencyPair": str,
        "baseCurrency": str,
        "quoteCurrency": str,
        "baseScale": int,
        "quoteScale": int,
        "baseStepAmount": str,
        "minOrderAmount": str,
        "maxOrderAmount": str,
        "makerTradeFeePercent": str,
        "takerTradeFeePercent": str,
        "closeOnly": bool,
        "viewOnly": bool,
        "enabled": bool,
    },
)


SymbolResponse: TypeAlias = list[SymbolObject]


TickerResponse: TypeAlias = TypedDict(
    "TickerResponse",
    {
        "symbolId": int,
        "bestAsk": str,
        "bestBid": str,
        "open": str,
        "high": str,
        "low": str,
        "last": str,
        "volume": str,
        "timestamp": int,
    },
)


AssetObject: TypeAlias = TypedDict(
    "AssetObject",
    {
        "currency": str,
        "onhandAmount": str,
    },
)


AssetResponse: TypeAlias = list[AssetObject]


Equityesponse: TypeAlias = TypedDict(
    "Equityesponse",
    {
        "floatingProfit": str,
        "floatingPositionFee": str,
        "remainingFloatingPositionFee": str,
        "floatingTradeFee": str,
        "floatingProfitAll": str,
        "usedMargin": str,
        "necessaryMargin": str,
        "balance": str,
        "equity": str,
        "marginMaintenancePercent": None,
        "usableAmount": str,
        "withdrawableAmount": str,
        "withdrawalAmountReserved": str,
    },
)


OrderObject: TypeAlias = TypedDict(
    "OrderObject",
    {
        "id": int,
        "symbolId": int,
        "orderBehavior": str,
        "orderSide": str,
        "orderPattern": str,
        "orderType": str,
        "closeBehavior": str,
        "price": str,
        "averagePrice": str,
        "amount": str,
        "remainingAmount": str,
        "orderStatus": str,
        "postOnly": bool,
        "oco1OrderId": None,
        "oco2OrderId": None,
        "positionId": None,
        "orderExpire": str,
        "expireBusinessDate": None,
        "leverage": str,
        "necessaryMargin": str,
        "businessDate": int,
        "orderCreatedAt": int,
        "createdAt": int,
        "updatedAt": int,
    },
)


OrderResponse: TypeAlias = list[OrderObject]
