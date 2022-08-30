import json
from aiohttp import ClientSession, MultipartWriter
from .const import ENDPOINT_URL
import datetime

class Api():
    _login = None
    _pass = None
    _session = None
    _token = None
    _cache = None
    _cacheTimestamp = datetime.datetime(datetime.MINYEAR, 1, 1)
    _cacheLifetime = datetime.timedelta(minutes=1)

    async def _doRequest(self, path, body):
        with MultipartWriter("form-data") as mp:
            part = mp.append(json.dumps(body))
            part.set_content_disposition('form-data', name='j')
            async with self._session.post(
                f'{ENDPOINT_URL}/{path}',
                data=mp,
            ) as resp:
                data = await resp.text()
        responseJson = json.loads(data)
        return responseJson

    async def refreshIfNeeded(self, force=False):
        if ((self._cacheTimestamp + self._cacheLifetime) < datetime.datetime.now()) or force:
            body = {"token": await self.getToken(), "list_start":0, "list_amount": 50, "local_id_object_type":[2,0],"iface_group":None,"branch":None,"local_id_object_group":[0,1,2],"connection":None,"sort":["system"]}
            responseJson = await self._doRequest('objects/list', body)
            self._cache = responseJson
            self._cacheTimestamp = datetime.datetime.now()

    async def getValue(self, id):
        await self.refreshIfNeeded()
        item = list(filter(lambda item:  item['id'] == id, self._cache['list']))[0]
        
        if 'value' in item['state']:
            return item['state']['value']['val']

        if 'state' in item['state']:
            return item['state']['state']['val']
            
        return item['state']['lk']['state_name']

    async def setState(self, id, state):
        body = {"token": await self.getToken(), "id_object": id, "state": state}
        responseJson = await self._doRequest('task/send_device_state', body)
        await self.refreshIfNeeded(True)

    async def getToken(self):
        if self._token is None:
            body = {'email': self._login, 'password': self._pass }
            responseJson = await self._doRequest('user/login', body)
            self._token = responseJson['token']
        return self._token

    async def getItems(self):
        await self.refreshIfNeeded()

        return list(self._cache['list'])

    def __init__(self, username: str, password: str, session: ClientSession):
        self._login = username
        self._pass = password
        self._session = session