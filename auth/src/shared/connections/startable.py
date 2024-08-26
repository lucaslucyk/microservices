import typing
from shared.connections.closable import Closable


class Startable(typing.Protocol):

    async def start_connection(self) -> Closable:
        """
        Starts a connections and returns a client that can be closed.
        """
        ...
