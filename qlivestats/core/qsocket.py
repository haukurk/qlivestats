import socket


class BaseSocketError(Exception):
    pass


class SocketConnectionError(BaseSocketError):
    pass


class SocketConnectionTimeoutError(BaseSocketError):
    pass


class BaseSocket(object):
    def __init__(self, broker):
        self.broker = broker 
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


class Socket(BaseSocket):
    def connect(self):
        try:
            self.socket.connect(self.broker)
        except socket.timeout, e:
            raise SocketConnectionTimeoutError('Timeout occured when connecting to UNIX socket (%s). Exception is %s' % (str(self.broker),str(e)))
        except socket.error, e:
            raise SocketConnectionError('Error when connecting to UNIX socket (%s). Exception is %s' % (str(self.broker),str(e)))
        return True

    def get(self, cmd):
        if self.connect():
            self.socket.send(cmd)
            self.close()
            return self.socket.recv(100000000)

    def close(self):
        self.socket.shutdown(socket.SHUT_WR)

