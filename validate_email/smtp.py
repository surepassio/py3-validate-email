import socks
import socket
import smtplib


class SocksSMTP(smtplib.SMTP):

    def __init__(self, host='', port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 source_address=None, proxy_type=None, proxy_addr=None, proxy_port=None, proxy_rdns=True,
                 proxy_username=None, proxy_password=None, socket_options=None):
        self._port = port
        self.proxy_type = proxy_type
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.proxy_rdns = proxy_rdns
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.socket_options = socket_options
        if self.proxy_type:
            self._get_socket = self.socks_get_socket
        super().__init__(host, port, local_hostname, timeout, source_address)

    def connect(self, host='localhost', port=0, source_address=None):
        return super().connect(host=host, port=port or self._port, source_address=source_address)

    def socks_get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socks.create_connection(
            (host, port), timeout=timeout, source_address=self.source_address, proxy_type=self.proxy_type,
            proxy_addr=self.proxy_addr, proxy_port=self.proxy_port, proxy_rdns=self.proxy_rdns,
            proxy_username=self.proxy_username, proxy_password=self.proxy_password, socket_options=self.socket_options)


class SocksSMTPSSL(smtplib.SMTP_SSL, SocksSMTP):

    pass
