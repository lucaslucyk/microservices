# import logging
from inspect import isawaitable
from typing import Any, Callable, Iterable, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult, DeleteResult
from bson.codec_options import CodecOptions


class MongoRepository:

    def __init__(
        self,
        url: str,
        db_name: str,
        min_pool_size: int,
        max_pool_size: int,
        max_idle_time: int,
        connect_timeout: int,
        wait_queue_timeout: int,
        server_selection_timeout: int,
        # logger: Optional[logging.Logger] = None,
    ) -> None:
        self.url = url
        self.db_name = db_name
        self.client = AsyncIOMotorClient(
            url,
            # in milliseconds
            maxIdleTimeMS=max_idle_time,
            # minimal pool size
            minPoolSize=min_pool_size,
            # maximal pool size
            maxPoolSize=max_pool_size,
            # connection timeout in miliseconds
            connectTimeoutMS=connect_timeout,
            # boolean
            retryWrites=False,
            # wait queue in miliseconds
            waitQueueTimeoutMS=wait_queue_timeout,
            # in miliseconds
            serverSelectionTimeoutMS=server_selection_timeout,
        )
        # self.logger = logger or logging.getLogger(__name__)

    def get_database(self) -> Database:
        return self.client[self.db_name]

    def get_collection(self, collection) -> Collection:
        return self.get_database().get_collection(
            collection, codec_options=CodecOptions(tz_aware=True)
        )

    async def drop(self, collection) -> None:
        await self.get_collection(collection).drop()

    def find_all_in(self, collection, query=None) -> Cursor:
        return self.get_collection(collection).find(query)

    async def find_one(self, collection: str, query: dict) -> Optional[Any]:
        return await self.get_collection(collection).find_one(query)

    async def insert_in(self, collection: str, data: dict, **kwargs):
        # Should return the save json. Data + id
        inserted_data = data.copy()
        result = await self.get_collection(collection).insert_one(
            data,
            **kwargs,
        )
        inserted_data["_id"] = result.inserted_id

        return inserted_data

    async def insert_many_in(
        self,
        collection: str,
        docs: Iterable[dict],
        **kwargs,
    ):
        await self.get_collection(collection).insert_many(docs, **kwargs)

    async def update_in(
        self,
        collection: str,
        data: dict,
        query: dict[str, Any],
        extra_operation: dict = {},
        **kwargs,
    ):
        _set = {"$set": data}
        full_operation = {**_set, **extra_operation}
        result: UpdateResult = await self.get_collection(collection).update_one(
            filter=query,
            update=full_operation,
            **kwargs,
        )

        if result.modified_count == 0:
            raise Exception(
                "Unable to update data. Perhaps it does not exist.",
                payload={"data": data, "query": query},
            )

    async def replace_in(
        self,
        collection: str,
        data: dict,
        query: dict[str, Any],
        **kwargs,
    ):
        coll = self.get_collection(collection)
        result: UpdateResult = await coll.replace_one(
            filter=query,
            replacement=data,
            **kwargs,
        )

        if result.modified_count == 0:
            raise Exception(
                "Unable to deplace data. Perhaps it does not exist.",
                payload={"data": data, "query": query},
            )

    async def delete_from(
        self,
        collection: str,
        query: dict[str, Any],
        **kwargs,
    ):
        result: DeleteResult = await self.get_collection(collection).delete_one(
            filter=query,
            **kwargs,
        )

        if result.deleted_count == 0:
            raise Exception(
                f"Unable to delete data on {collection} with query: {query}",
                payload={"query": query},
            )

    async def find_one_and_update(
        self,
        collection: str,
        data: dict,
        query: dict[str, Any],
        return_document: str,
        **kwargs,
    ):
        operation = {"$set": data}
        return await self.get_collection(collection).find_one_and_update(
            filter=query,
            update=operation,
            return_document=return_document,
            **kwargs,
        )

    async def with_transaction(self, callable: Callable):
        async with await self.client.start_session() as s:
            async with s.start_transaction():
                result = callable()
                if isawaitable(result):
                    result = await result
                await s.commit_transaction()
                await s.end_session()

    async def close(self):
        self.client.close()
