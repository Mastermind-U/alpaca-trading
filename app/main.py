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
    return await alpaca.post_order(OrderPlaceRequest(
        symbol=data.ticker,
        notional=100,
        side="buy",
        type="limit",
        time_in_force="gtc",
        limit_price=data.close,
        order_class="simple",
        take_profit=Profit(limit_price=data.close * 1.01),
        stop_loss=StopLoss(stop_price=data.close * .98),
    ))
