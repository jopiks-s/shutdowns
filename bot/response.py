from dataclasses import dataclass, field
from typing import Optional, Tuple

from bot.commands import Commands


@dataclass(frozen=True)
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str


@dataclass(frozen=True)
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None


@dataclass(frozen=True)
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    date: int
    text: Optional[str] = None
    command: Optional[Commands] = None
    parameters: Optional[Tuple[str, ...]] = field(default_factory=lambda: [])


@dataclass(frozen=True)
class ResultObj:
    update_id: int
    message: Message


@dataclass(frozen=True)
class GetUpdatesResponse:
    ok: bool
    result: Tuple[ResultObj, ...]
