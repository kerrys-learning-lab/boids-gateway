import asyncio
import datetime
import logging
import pytest
import aiohttp.web_request
import boids
import boidsapi.model
import boids_utils.elastic
import boids_utils.openapi
import boids_utils.pubsub
import boids.gateway.controllers.session
import boids.gateway.openapi.session

LOGGER = logging.getLogger(__name__)

class Consumer(boids_utils.pubsub.ConsumerCallback):
    def __init__(self) -> None:
       self._event = asyncio.Event()
       self.message = None

    def on_message(self, message: boids_utils.pubsub.Message):
        self.message = message
        self._event.set()

    async def wait(self):
       await self._event.wait()

@pytest.mark.asyncio
@pytest.mark.timeout(60)
async def test_create(test_pubsub_broker: boids_utils.pubsub,
                      test_openapi_spec,
                      test_elasticsearch: boids_utils.elastic,
                      aiohttp_client):
    listener = Consumer()
    boids_utils.pubsub.add_topic_callback('boids.sessions', listener)

    connexion_app = boids.create_app()
    aiohttp_app = connexion_app.app

    client = await aiohttp_client(aiohttp_app)

    session_config = {
        'title': f'{__name__}.test_create',
        'num_boids': 10
    }

    async with client.post('/api/v1/session', json=session_config) as response:

        created_json = await response.json()
        created_obj = boidsapi.model.SessionConfigurationStatus.from_dict(created_json)
        LOGGER.debug(f'created: {created_json}')

        now = boids_utils.nowutc()

        assert created_obj.uuid is not None
        assert created_obj.title == session_config['title']
        assert created_obj.num_boids == session_config['num_boids']
        assert created_obj.url.endswith(f'/api/v1/session/{created_obj.uuid}')

        timedelta_created: datetime.timedelta = boids_utils.str_to_datetime(created_obj.created) - now
        assert timedelta_created.total_seconds() < 5

        timedelta_modified: datetime.timedelta = boids_utils.str_to_datetime(created_obj.modified) - now
        assert timedelta_modified.total_seconds() < 5

        await listener.wait()
        assert listener.message.value['uuid'] == created_obj.uuid
