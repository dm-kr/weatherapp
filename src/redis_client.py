import json

from redis.asyncio import Redis


class RedisClient:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = Redis(host='redis')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def get(self, key):
        data = await self.client.get(key)
        if data:
            return json.loads(data)

    async def set(self, key, data, ex=60):
        await self.client.set(key, json.dumps(data), ex=ex)
