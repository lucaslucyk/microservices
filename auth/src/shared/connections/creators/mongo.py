from typing import Optional
from shared.connections.startable import Startable
from shared.connections.repositories.mongo.client import MongoRepository
from shared.conf import Settings


class MongoClientCreator(Startable):

    def __init__(
        self,
        url: str,
        db_name: str,
        config: Optional[Settings] = Settings(),
    ) -> None:
        self.url = url
        self.db_name = db_name
        self._cfg = config

    async def start_connection(self) -> MongoRepository:
        return MongoRepository(
            url=self.url,
            db_name=self.db_name,
            min_pool_size=self._cfg.MONGO_MIN_POOL_SIZE,
            max_pool_size=self._cfg.MONGO_MAX_POOL_SIZE,
            max_idle_time=self._cfg.MONGO_MAX_IDLE_TIME,
            connect_timeout=self._cfg.MONGO_CONNECT_TIMEOUT,
            wait_queue_timeout=self._cfg.MONGO_WAIT_QUEUE_TIMEOUT,
            server_selection_timeout=self._cfg.MONGO_SERVER_SELECTION_TIMEOUT,
        )
