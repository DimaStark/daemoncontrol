from typing import Iterable, Optional

from abc import ABC, abstractstaticmethod
from collections import namedtuple

DaemonInfo = namedtuple('DaemonInfo', ['pid', 'status', 'name'])


class ParseError(Exception):
    pass


class ProcessError(Exception):
    pass


class DaemonControl(ABC):
    @staticmethod
    @abstractstaticmethod
    async def which() -> str:
        pass

    @staticmethod
    @abstractstaticmethod
    async def list() -> Iterable[DaemonInfo]:
        pass

    @staticmethod
    @abstractstaticmethod
    async def info(daemon_name: str) -> Optional[DaemonInfo]:
        pass

    @staticmethod
    @abstractstaticmethod
    async def start(daemon_name: str) -> str:
        pass

    @staticmethod
    @abstractstaticmethod
    async def stop(daemon_name: str) -> str:
        pass

    @staticmethod
    @abstractstaticmethod
    async def restart(daemon_name: str) -> str:
        pass
