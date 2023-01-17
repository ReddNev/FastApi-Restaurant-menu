import decimal

from pydantic import BaseModel, Field


class BaseBody(BaseModel):
    title: str = Field(max_length=255, default=None)
    description: str = Field(default=None)


class BodyMenu(BaseBody):
    pass


class BodySubMenu(BaseBody):
    pass


class BodyDish(BaseBody):
    price: decimal.Decimal = Field(max_digits=18, decimal_places=2)


class BaseResponse(BaseModel):
    id: int


class ResponseSubMenu(BaseResponse, BodySubMenu):
    menuId: int
    dishCount: int = Field(default=0)


class ResponseMenu(BaseResponse, BodyMenu):
    submenuCount: int = Field(default=0)
    dishCount: int = Field(default=0)


class ResponseDish(BaseResponse, BodyDish):
    submenuId: int
