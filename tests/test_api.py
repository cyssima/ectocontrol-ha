
import asyncio
from custom_components.ectocontrol.api import Api

def await_(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

def test_login():
    sensor = Api('test', 'test', ClientSession())
    value = await_(sensor.getValue(20605))
    items = await_(sensor.getItems())
    print(items)
    assert value > 10