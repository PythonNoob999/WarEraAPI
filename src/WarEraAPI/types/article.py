from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import ARTICLE_CATEGORY
from WarEraAPI.types.constants import ArticleStats
from WarEraAPI.utils import edit_types


@dataclass
class Article:

    _id: str
    title: str
    stats: ArticleStats
    content: str | None = field(default=None)
    language: str | None = field(default=None)
    category: ARTICLE_CATEGORY | None = field(default=None)
    author: str | None = field(default=None)
    isPublished: bool | None = field(default=None)
    isDeleted: bool | None = field(default=None)
    createdAt: datetime | None = field(default=None)
    updatedAt: datetime | None = field(default=None)
    publishedAt: datetime | None = field(default=None)
    isPublic: bool | None = field(default=None)
    slug: str | None = field(default=None)
    welcomeArticleOfCountry: bool | None = field(default=None)


    def __post_init__(self):

        edit_types(self)