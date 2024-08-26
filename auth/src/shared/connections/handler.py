from typing import Any
from shared.connections.startable import Startable
from shared.connections.closable import Closable
from shared.connections.repositories.mongo.client import MongoRepository


class ConnectionsHandler:

    def __init__(self, creators: dict[str, Startable]):
        self.creators = creators
        self.clients: dict[str, Closable] = dict()

    async def start_connections(self):
        for k, creator in self.creators.items():
            client = await creator.start_connection()
            self.clients[k] = client

    async def close_connections(self):
        for client in self.clients.values():
            await client.close()

    def get_client(self, name: str) -> Closable:
        client = self.clients.get(name, None)

        if client is None:
            raise KeyError(f"Unknown connection: {name}")

        return client

    def get_kind_client(self, kind: Any, index: int = 0) -> Closable:
        """
        Returns a client of the specified kind from the clients dictionary.

        Args:
            kind (Any): The type of client to retrieve.
            index (int, optional): The index of the client to retrieve if multiple clients of the same kind exist. Defaults to 0.

        Returns:
            Closable: The client of the specified kind.

        Raises:
            KeyError: If no client of the specified kind is found in the clients dictionary.
        """

        matches: list[Closable] = list(
            filter(lambda c: isinstance(c, kind), self.clients.values())
        )
        if not matches:
            raise KeyError(f"No registered client of type {kind}")

        return matches[index]

    @property
    def mongo_client(self) -> MongoRepository:
        return self.get_kind_client(MongoRepository)
