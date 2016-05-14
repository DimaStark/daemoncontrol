"""Daemon class"""


from subprocess import Popen, PIPE


class Daemon:
    """Daemon class. Need root"""
    def __init__(self, name):
        self.name = name

    @staticmethod
    def _exec(name, com):
        """Exec command for daemon with 'name'"""
        return Popen(["sudo", "service", name, com], 
                     stdout=PIPE, stderr=PIPE)

    def stop(self):
        """Stop daemon"""
        return self._exec(self.name, "stop").wait()
    
    def restart(self):
        """Restart daemon"""
        return self._exec(self.name, "restart").wait()

    @staticmethod
    def getdaemonstatus(name):
        """Get status of daemon with 'name'"""
        out = Daemon._exec(name, "status").stdout
        data = out.read().decode()
        lind = data.find("Active: ") + len("Active: ")
        shift = data[lind:].find(" ")
        return data[lind:lind + shift]

    @property
    def status(self):
        """Status of current daemon"""
        return self.getdaemonstatus(self.name)
