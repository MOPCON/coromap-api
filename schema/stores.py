from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyHttpUrl, Field


class StoreData(BaseModel):
    """
    Properties to create store
    """
    url: AnyHttpUrl
    last_updated_at: Optional[datetime] = Field(
        None, description='最後更新時間', example=1621867382
    )
    open: str = Field(
        ..., description='是否繼續維持營業', example='是'
    )
    inside: str = Field(
        ..., description='是否能提供內用服務', example='是'
    )
    outside: str = Field(
        ..., description='是否提供外帶', example='是'
    )
    delivery: str = Field(
        ..., description='是否提供外送', example='是'
    )
    discount: str = Field(
        ..., description='防疫外帶 / 外送優惠'
    )
    seat_change: str = Field(
        ..., description='內用座位調整情況'
    )
    open_time_change: str = Field(
        ..., description='營業時間調整'
    )
    prevention_measures: str = Field(
        ..., description='店家防疫措施'
    )
