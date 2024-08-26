import typing


class Closable(typing.Protocol):

    async def close(self) -> None:
        """
        Closes the connection.
        """
        ...