from dataclasses import dataclass
from typing import List, Optional
from bot_lib.commands import Commands


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str


@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None


@dataclass
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    date: int
    text: Optional[str] = None
    command: Optional[Commands] = None
    parameters: Optional[List[str]] = None


@dataclass
class ResultObj:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[ResultObj]
