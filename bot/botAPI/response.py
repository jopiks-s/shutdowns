from dataclasses import dataclass, field
from typing import Tuple, Any

from bot.botAPI._commands import Commands


@dataclass(frozen=True)
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


@dataclass(frozen=True)
class Chat:
    id: int
    type: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    title: str | None = None


@dataclass(frozen=True)
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    date: int
    text: str | None = None
    command: Commands | None = None
    parameters: Tuple[Any, ...] | None = field(default_factory=lambda: [])


@dataclass(frozen=True)
class ResultObj:
    update_id: int
    message: Message


@dataclass(frozen=True)
class GetUpdatesResponse:
    ok: bool
    result: Tuple[ResultObj, ...]


@dataclass(frozen=True)
class Updates:
    messages: Tuple[Message, ...]
    last_update_id: int


@dataclass(frozen=True)
class PackedUpdate:
    id: int
    messages: Tuple[Message, ...]
