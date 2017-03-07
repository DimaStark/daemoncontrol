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

    def all_services(self):
        return self.states.keys()

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

    def _state_to_html(self, name):
        status = self.status(name)
        html_class = 'on' if status else 'off'
        status_char = '+' if status else '-'
        return r'''
            <tr class="{}">
                <td>{}</td>
                <td>{}</td>
                <td><button>Старт</button></td>
                <td><button>Стоп</button></td>
                <td><button>Рестарт</button></td>
                <td><button>Принудительная перезагрузка</button></td>
            </tr>
        '''.format(html_class, name, status_char)

    def to_html(self):
        names = sorted(self.states.keys())
        return ''.join(map(self._state_to_html, names))
