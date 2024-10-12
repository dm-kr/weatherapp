import aiohttp


class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        })
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get(self, endpoint, params=None):
        url = f'{self.base_url}{endpoint}'
        async with self.session.get(url, params=params) as response:
            return await self._handle_response(response)

    async def _handle_response(self, response):
        if response.status == 200:
            return await response.json()
        else:
            response.raise_for_status()


class Resource:
    def __init__(self, client: APIClient, resource_path: str):
        self.client = client
        self.resource_path = resource_path

    async def get(self, params=None):
        return await self.client.get(self.resource_path, params=params)
