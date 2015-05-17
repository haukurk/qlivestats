import socket


class BaseSocketError(Exception):
    pass


class SocketConnectionError(BaseSocketError):
    pass


class SocketConnectionTimeoutError(BaseSocketError):
    pass


class BaseSocket(object):
    def __init__(self, cfg):
        self.broker = cfg.get_broker()
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


class Socket(BaseSocket):
    def connect(self):
        try:
            self.socket.connect(self.broker)
        except socket.timeout, e:
            raise SocketConnectionTimeoutError('Timeout occured when connecting to UNIX socket (%s). Exception is %s' % (str(self.broker),str(e)))
        except socket.error, e:
            raise SocketConnectionError('Error when connecting to UNIX socket (%s). Exception is %s' % (str(self.broker),str(e)))
    
    def close(self):
        self.socket.close()

