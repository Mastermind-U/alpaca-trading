"""Datamap for requests and responses."""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.types import constr

OrderType = Literal[  # noqa: A003
    "market", "limit",
    "stop", "stop_limit",
    "trailing_stop",
]
TimeInForce = Literal["day", "gtc", "cls", "ioc", "fok"]
SideType = Literal["buy", "sell"]
OrderClass = Literal["simple", "bracket", "oco", "oto"]


class OrderListRequest(BaseModel):
    """Request datamap."""

    status: Literal['open', 'closed', 'all']
    limit: int
    after: float
    until: float
    direction: Literal['asc', 'desc']
    nested: bool
    symbols: list[str]


class Profit(BaseModel):
    """Additional parameters for take-profit leg of advanced orders."""

    limit_price: int


class StopLoss(BaseModel):
    """Additional parameters for stop-loss leg of advanced orders."""

    stop_price: int
    limit_price: Optional[int] = None


class OrderPlaceRequest(BaseModel):
    """Place order request body."""

    symbol: str
    qty: Optional[int]
    notional: Optional[int]
    side: SideType
    type: OrderType  # noqa: A003
    time_in_force: TimeInForce
    limit_price: Optional[int] = None
    stop_price: Optional[int] = None
    trail_price: Optional[int] = None
    trail_percent: Optional[int] = None
    extended_hours: bool = False
    client_order_id: Optional[constr(max_length=48)]  # type: ignore
    order_class: OrderClass
    take_profit: Profit
    stop_loss: StopLoss


class Order(BaseModel):
    """Order representation."""

    id: UUID  # noqa: A003
    client_order_id: UUID
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime
    filled_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    replaced_at: Optional[datetime] = None
    replaced_by: Optional[UUID] = None
    replaces: Optional[UUID] = None
    asset_id: UUID
    symbol: str
    asset_class: str  # "us_equity"
    notional: Optional[int]
    qty: Optional[float]
    filled_qty: Optional[int] = 0
    filled_avg_price: Optional[float]
    order_class: OrderClass
    order_type: Optional[str] = None
    type: OrderType  # noqa: A003
    side: SideType
    time_in_force: TimeInForce
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    status: Literal[
        "accepted", "new", "partially_filled", "filled",
        "done_for_day", "canceled", "expired",
        "replaced", "pending_cancel", "pending_replace",
    ]
    extended_hours: bool
    legs: Optional["Order"]
    trail_percent: Optional[int]
    trail_price: Optional[int]
    hwm: Optional[int]


class OrderWebhookData(BaseModel):
    """Data from webhook."""

    open: float  # noqa: A003
    high: float
    low: float
    close: float
    exchange: str
    ticker: str
    volume: float
    time: datetime
    timenow: datetime
