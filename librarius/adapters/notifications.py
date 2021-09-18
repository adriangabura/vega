import typing as tp
import abc


class AbstractNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError


DEFAULT_HOST = 'https://mock'
DEFAULT_PORT = 6666


class MemoryNotification(AbstractNotification):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = []

    def send(self, destination, message) -> None:
        msg = f"Subject: some notification \n {message}"
