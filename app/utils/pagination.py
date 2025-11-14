from math import ceil
from typing import Sequence, TypeVar

T = TypeVar("T")


def paginate(items: Sequence[T], page: int = 1, page_size: int = 10) -> dict[str, object]:
    start = (page - 1) * page_size
    end = start + page_size
    slice_ = items[start:end]
    total_pages = ceil(len(items) / page_size) or 1
    return {
        "items": slice_,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
