from typing import NamedTuple, Optional


class Person(NamedTuple):
    vk_id: int
    first_name: str
    last_name: str
    link: str
    can_access_closed: bool
    is_closed: bool


class Photo(NamedTuple):
    owner_id: int
    popular: int
    photo: Optional[str]
