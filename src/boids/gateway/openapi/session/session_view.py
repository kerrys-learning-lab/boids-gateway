""" Defines async HTTP CRUD operations for Sessions """
import aiohttp
import aiohttp.web_exceptions
import aiohttp.web_request
import aiohttp.web_response
import aiohttp.web
import boidsapi.model
import boids_utils.openapi
import boids.gateway.controllers.session

class SessionView:
    """ Defines async HTTP CRUD operations for Sessions """

    FIELD_REQUIREMENTS = {
        'post': {
            'must': ['title', 'num_boids'],
            'must_not': ['state']
        }
    }

    async def search(self, title: str = None, state: str = None, uuid: str = None, **kwargs):
        """
        Searches for Sessions matching the given combination of title, state,
        uuid, etc.
        """
        pagination = boidsapi.model.Pagination.from_dict(kwargs)
        state = boids_utils.openapi.to_SessionState(state)

        result = await boids.gateway.controllers.session.search(title=title,
                                                                state=state,
                                                                entity_id=uuid,
                                                                pagination=pagination)
        return aiohttp.web.json_response(result.to_dict())

    async def get(self, uuid: str = None):
        """ Returns the Session identified by the given UUID """
        try:
            result = await boids.gateway.controllers.session.get(uuid)

            return aiohttp.web.json_response(result.to_dict())
        except Exception as ex:
            raise aiohttp.web_exceptions.HTTPNotFound(text=str(ex))

    async def post(self,
                   body: dict = None,
                   request: aiohttp.web_request.Request = None):
        """ Creates a new Session """
        self._assert_fields('post', body)
        config = boidsapi.model.SessionConfiguration.from_dict(body)

        result = await boids.gateway.controllers.session.create(config, request.url)

        return aiohttp.web.json_response(result.to_dict())

    async def put(self,
                  uuid: str = None,
                  body: dict = None,
                  request: aiohttp.web_request.Request = None):
        """ Modifies an existing Session """
        self._assert_fields('put', body)
        config = boidsapi.model.SessionConfiguration.from_dict(body)

        result = await boids.gateway.controllers.session.modify(uuid, config, request.url)

        return aiohttp.web.json_response(result.to_dict())

    async def delete(self):
        """ Deletes a Session """

    def _assert_fields(self, http_op: str, data: dict) -> None:
        must = SessionView.FIELD_REQUIREMENTS.get(http_op, {}).get('must', [])
        missing = []
        for field in must:
            if field not in data:
                missing.append(field)

        if missing:
            missing = ','.join(missing)
            raise aiohttp.web_exceptions.HTTPBadRequest(text=f'Missing required field(s) for {http_op}: {missing}')

        must_not = SessionView.FIELD_REQUIREMENTS.get(http_op, {}).get('must_not', [])
        present = []
        for field in must_not:
            if field in data:
                present.append(field)

        if present:
            present = ','.join(present)
            raise aiohttp.web_exceptions.HTTPBadRequest(text=f'Extra field(s) not allowed for {http_op}: {present}')
