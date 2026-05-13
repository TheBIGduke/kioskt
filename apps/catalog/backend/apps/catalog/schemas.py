# Made by Kaléin Tamaríz
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ProductMediaSchema(BaseModel):
    media_url: str
    is_primary: bool
    position: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class CategorySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]
    categories: List[str]
    media: List[ProductMediaSchema]
    primary_image: Optional[str]

    model_config = ConfigDict(from_attributes=True)
