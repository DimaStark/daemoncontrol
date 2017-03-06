import re
import asyncio
from asyncio.subprocess import create_subprocess_exec, PIPE


class Service:
    """ Wrapper for bash service """
    status_re = re.compile(' \[ ([+-]) ]  ([\w\-.]+)')
    opposites = {'start': 'stop', 'stop': 'start'}

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.states = {}
        self.update_states()

    @staticmethod
    def _exec(*params):
        """ Execute service command in subprocess """
        args = ['sudo', 'service'] + list(params)
        return create_subprocess_exec(*args, stdin=PIPE, stdout=PIPE)

    def update_states(self):
        statuses = self.loop.run_until_complete(self.status_all())
        self.states = {i[1]: i[0] == '+' for i in statuses}

    async def change_daemon(self, name, command, before, after):
        if self.states[name] == after != before:
            return '{} already {}ed'.format(name, command)
        if self.states[name] != before != after:
            return '{} is not {}ed'.format(name, self.opposites[command])
        await Service._exec(name, command).wait()
        self.update_states()
        if self.states[name] == after:
            return 'Success to {} a {} daemon'.format(command, name)
        return 'Failed to {} a {} daemon'.format(command, name)

    async def status_all(self):
        proc = await self._exec('--status-all')
        stdout, *_ = await proc.communicate()
        output = bytes(stdout).decode()
        return self.status_re.findall(output)

    async def start(self, name):
        return await self.change_daemon(name, 'start', '-', '+')

    async def stop(self, name):
        return await self.change_daemon(name, 'stop', '+', '-')

    async def restart(self, name):
        return await self.change_daemon(name, 'restart', '+', '+')

    async def force_reload(self, name):
        return await self.change_daemon(name, 'force-reload', '+', '+')

    def status(self, name):
        return self.states[name]


class Daemon:
    def __init__(self, name, service=Service()):
        self.service = service
        self.name = name

    async def start(self):
        """Stop daemon"""
        return await self.service.start(self.name)

    async def stop(self):
        """Stop daemon"""
        return await self.service.stop(self.name)

    async def restart(self):
        """Restart daemon"""
        return await self.service.restart(self.name)

    @property
    async def status(self):
        """Status of current daemon"""
        return await self.service.status(self.name)
