from typing import Iterable, Optional
from shutil import which

from .util import exec_su, forgive_error
from .control import DaemonControl, DaemonInfo, ParseError


class LaunchCtl(DaemonControl):
    name = 'launchctl'

    @staticmethod
    async def which() -> Optional:
        return which(LaunchCtl.name)

    @staticmethod
    async def list() -> Iterable[DaemonInfo]:
        output = await exec_su(f'{LaunchCtl.name} list')
        lines = output.split('\n')

        return filter(bool, (LaunchCtl._parse_info(l) for l in lines))

    @staticmethod
    async def info(daemon_name) -> Optional[str]:
        output = await exec_su(f'{LaunchCtl.name} list | grep {daemon_name}')

        return LaunchCtl._parse_info(output)

    @staticmethod
    async def start(daemon_name) -> str:
        return await exec_su(f'{LaunchCtl.name} load -w {daemon_name}')

    @staticmethod
    async def stop(daemon_name) -> str:
        return await exec_su(f'{LaunchCtl.name} unload {daemon_name}')

    @staticmethod
    async def restart(daemon_name) -> str:
        stop_output = await LaunchCtl.stop(daemon_name)
        start_output = await LaunchCtl.start(daemon_name)

        return f'{start_output}\n{stop_output}'

    @staticmethod
    @forgive_error(ParseError)
    def _parse_info(raw: str) -> DaemonInfo:
        try:
            pid, status, name = raw.split('\t')

            return DaemonInfo(pid, status, name)
        except AttributeError:
            raise ParseError()
