import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth.routers import ping, users
from shared.connections.handler import ConnectionsHandler
from shared.connections.creators.mongo import MongoClientCreator
from shared.connections.startable import Startable


class ColoredFormatter(logging.Formatter):
    # Código de escape ANSI para color azul
    BLUE = "\033[34m"
    RESET = "\033[0m"

    def format(self, record):
        # Aplica el color azul al levelname y resetea el color
        record.levelname = f"{self.BLUE}{record.levelname}{self.RESET}"
        return super().format(record)


class Logger:

    @staticmethod
    def create(
        name: str = __name__,
        level: int = logging.INFO,
    ) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        stream_handler = logging.StreamHandler(sys.stdout)
        log_formatter = ColoredFormatter(
            "%(levelname)s [%(name)s]: %(message)s"
        )
        stream_handler.setFormatter(log_formatter)
        logger.addHandler(stream_handler)
        return logger


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # , lifespan=App.lifespan)
        self.logger = Logger.create()
        self._creators: dict[str, Startable] = None
        self.connections: ConnectionsHandler = None

        self.add_event_handler("startup", self.configure)
        self.add_event_handler("shutdown", self.close)

        self.include_router(ping.router)
        self.include_router(users.router)

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: "App"):
        await app.configure()
        # lifecicle
        yield

        await app.close()

    async def configure(self):
        self.logger.info("Configuring app...")
        self._creators = {
            "mongo": MongoClientCreator(
                url="mongodb://root:C0m.pl3x@localhost:31017",
                db_name="msv_auth",
            )
        }
        self.connections = ConnectionsHandler(creators=self._creators)
        await self.connections.start_connections()
        self.logger.info("Connections started!")

    async def close(self):
        await self.connections.close_connections()
        self.logger.info("Connections closed!")
