from pythonping import ping

class ClusterNode:
    ip_address=None
    status=False

    def __init__(self, ip, powerbutton=None, resetbutton=None, statuslabel=None):
        self.ip_address=ip
        self.resetbutton=resetbutton
        self.powerbutton=powerbutton

    def getpingresult(self):
        reply=str(ping(self.ip_address, count=1))
        return reply.startswith('Reply from ' + self.ip_address)

    def updatestatus(self):
        self.status=self.getpingresult()
