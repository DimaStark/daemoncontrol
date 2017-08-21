from typing import ClassVar

from asyncio.subprocess import create_subprocess_exec, PIPE

from .control import DaemonControl
from .launchctl import LaunchCtl


async def exec_cp(cmd: str) -> str:
    return await create_subprocess_exec(
        cmd.split(),
        stdout=PIPE,
        stderr=PIPE
    )


async def exec_su(cmd: str) -> str:
    return await exec_cp(f'sudo {cmd}')


def forgive_error(ErrorClass: ClassVar[Exception]):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except ErrorClass:
                return None

        return wrapped_function

    return decorator


def get_daemon_controller() -> ClassVar[DaemonControl]:
    controllers: ClassVar[DaemonControl] = [
        LaunchCtl
    ]

    for Controller in controllers:
        if Controller.which():
            return Controller

    raise AttributeError('System Daemon manager not found')
