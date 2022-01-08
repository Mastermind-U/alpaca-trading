"""Alpaca api code."""

from typing import Any, Literal

from httpx import AsyncClient
from loguru import logger
from pydantic import ValidationError
from settings import get_settings

from .models import Order, OrderListRequest, OrderPlaceRequest

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

    class APIException(Exception):
        """API re raise exc."""

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
        if response.status_code != 200:
            raise self.APIException(response.json())
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
        try:
            return Order(**response)
        except ValidationError as err:
            logger.error(err)
