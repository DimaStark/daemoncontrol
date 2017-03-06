from .service import Service


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
