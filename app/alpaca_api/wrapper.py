"""Alpaca api code."""

from functools import lru_cache
from typing import Any, Literal

from httpx import AsyncClient
from pydantic import BaseModel, SecretStr

from .models import Order, OrderListRequest, OrderPlaceRequest


class Settings(BaseModel):
    """Base settings model."""

    DEBUG: bool = True
    ALPACA_API_KEY_ID: SecretStr
    ALPACA_SECRET_KEY: SecretStr


@lru_cache
def get_settings() -> Settings:
    """Generate settings."""
    return Settings(  # noqa: S106
        ALPACA_API_KEY_ID="PKT3M5D3K2FG0HXSB3TV",
        ALPACA_SECRET_KEY="gRzbv7Ag1Uy2F0wuqcVJ1nzK2UiS2WgEpAu93Mq1",
    )


settings = get_settings()


class MarketURLs:
    """Market endpoint list."""

    MARKET_CRYP_DATA = "https://data.alpaca.markets/v1beta1/crypto"
    MARKET_CRYP_DATA_ALIVE = "wss://stream.data.alpaca.markets/v1beta1/crypto"


class AlpacaMap:
    """Alpaca endpoints list."""

    ACCOUNT = "/v2/account"
    ORDERS = "/v2/orders"


class AlpacaAPI:
    """Alpaca api interface."""

    BASE_PAPER_URL: str = "https://paper-api.alpaca.markets"
    BASE_LIVE_URL: str = "https://api.alpaca.markets"

    def __init__(self):
        """Set up debug key."""
        if settings.DEBUG:
            self.url = self.BASE_PAPER_URL
        else:
            self.url = self.BASE_LIVE_URL
        self.client = AsyncClient(base_url=self.url)

    async def _make_request(
        self, url: str,
        rtype: Literal['POST', 'GET', 'DELETE'],
        data: dict,
    ) -> Any:
        response = await self.client.request(
            rtype, url, json=data,
            headers={  # type: ignore
                "APCA-API-KEY-ID": settings.ALPACA_API_KEY_ID,
                "APCA-API-SECRET-KEY": settings.ALPACA_SECRET_KEY,
            },
        )

        return response.json()

    async def orders(self, data: OrderListRequest) -> list[Order]:
        """Get order batch.

        :param data: request data
        :type data: OrderListRequest
        :return: order batch
        :rtype: list[Order]
        """
        response: list[dict] = await self._make_request(
            AlpacaMap.ORDERS, "GET", data.dict())
        return [Order(**order) for order in response]

    async def post_order(self, data: OrderPlaceRequest) -> Order:
        """Place order, buy stocks."""
        response: dict = await self._make_request(
            AlpacaMap.ORDERS, "POST", data.dict())
        return Order(**response)
