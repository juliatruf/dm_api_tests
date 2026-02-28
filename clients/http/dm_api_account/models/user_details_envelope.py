from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class Info(BaseModel):
    value: Optional[str] = Field(None, alias='value')
    parse_mode: List[BbParseMode] = Field(None, alias='parseMode')


class Paging(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: Union[List[ColorSchema], ColorSchema, None] = Field(None, alias='colorSchema')
    nanny_greetings_message: Optional[str] = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: Optional[str] = Field(None, alias='mediumPictureUrl')
    small_picture_url: Optional[str] = Field(None, alias='smallPictureUrl')
    status: Optional[str] = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: Optional[str] = Field(None, alias='name')
    location: Optional[str] = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')
    icq: Optional[str] = Field(None, alias='icq')
    skype: Optional[str] = Field(None, alias='skype')
    original_picture_url: Optional[str] = Field(None, alias='originalPictureUrl')
    info: Union[Info, str, None]
    settings: Settings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
