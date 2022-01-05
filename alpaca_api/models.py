"""Datamap for requests and responses."""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class OrderListRequest(BaseModel):
    """Request datamap."""

    status: Literal['open', 'closed', 'all']
    limit: int
    after: float
    until: float
    direction: Literal['asc', 'desc']
    nested: bool
    symbols: list[str]


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
    qty: Optional[int]
    filled_qty: Optional[int] = 0
    filled_avg_price: int
    order_class: Literal["simple", "bracket", "oco", "oto"]
    order_type: Optional[str] = None
    type: Literal[  # noqa: A003
        "market", "limit",
        "stop", "stop_limit",
        "trailing_stop",
    ]
    side: Literal["buy", "sell"]
    time_in_force: Literal["day", "gtc", "cls", "ioc", "fok"]
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    status: Literal[
        "new", "partially_filled", "filled",
        "done_for_day", "canceled", "expired",
        "replaced", "pending_cancel", "pending_replace",
    ]
    extended_hours: bool
    legs: Optional["Order"]
    trail_percent: int
    trail_price: int
    hwm: int
