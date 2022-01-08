"""Main web app."""

from alpaca_api.models import (
    OrderPlaceRequest,
    OrderWebhookData,
    Profit,
    StopLoss,
)
from alpaca_api.wrapper import AlpacaAPI
from fastapi import FastAPI

app = FastAPI()
alpaca = AlpacaAPI()


@app.post('/make_request')
async def make_order(data: OrderWebhookData):
    """Entry webhook.

    {
        "open": {{open}},
        "high": {{high}},
        "low": {{low}},
        "close": {{close}},
        "exchange": "{{exchange}}",
        "ticker": "{{ticker}}",
        "volume": {{volume}},
        "time": "{{time}}",
        "timenow": "{{timenow}}"
    }
    """
    # alpaca.post_order(OrderPlaceRequest(
    #     extended_hours=None
    # ))
    return data
