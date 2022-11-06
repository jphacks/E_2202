from enum import (
    Enum,
    auto,
)
from typing import (
    Any,
)

from pydantic import (
    BaseModel,
)
from pydantic.dataclasses import dataclass


class TextType(Enum):
    ERROR_MESSAGE = auto()
    LIBRARY_NAME = auto()
    ERROR_OCCURS_ROW_IN_CODE = auto()


class ORMConfig:
    orm_mode = True


@dataclass(config=ORMConfig)
class TextIndices:
    start: int
    end: int  # end - 1 が python の index


@dataclass(config=ORMConfig)
class HighlightTextInfo:
    row_idx: int
    col_idxes: TextIndices
    text: str
    type: TextType

    def __lt__(self, other: Any) -> Any:
        if not isinstance(other, HighlightTextInfo):
            NotImplementedError(f"HighlightInfo and {type(other)} are not implemented < operator.")
        return self.row_idx < other.row_idx


class ErrorContents(BaseModel):
    language: str
    error_text: str


class ImportantErrorLines(BaseModel):
    result: list[HighlightTextInfo]
