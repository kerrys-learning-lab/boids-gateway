"""
Business-logic used by web-views for Session CRUD operations.
"""
import logging
import yarl
import boids_api.boids
import boids_utils
import boids_utils.elastic
import boids_utils.openapi
import boids_utils.pubsub

LOGGER = logging.getLogger('session')

SESSIONS_TOPIC = 'boids.sessions'

NEXT_STATES = {
    boids_api.boids.SessionState.PENDING: [],
    boids_api.boids.SessionState.PAUSED: [
      boids_api.boids.SessionState.RESET,
      boids_api.boids.SessionState.RUNNING,
      boids_api.boids.SessionState.STEP,
      boids_api.boids.SessionState.TERMINATED
    ],
    boids_api.boids.SessionState.RESET: [
      boids_api.boids.SessionState.RUNNING,
      boids_api.boids.SessionState.STEP,
      boids_api.boids.SessionState.TERMINATED,
      boids_api.boids.SessionState.ARCHIVED
    ],
    boids_api.boids.SessionState.RUNNING: [
      boids_api.boids.SessionState.PAUSED,
      boids_api.boids.SessionState.STEP,
      boids_api.boids.SessionState.TERMINATED
    ],
    boids_api.boids.SessionState.STEP: [
        boids_api.boids.SessionState.PAUSED,
        boids_api.boids.SessionState.RUNNING,
        boids_api.boids.SessionState.TERMINATED
    ],
    boids_api.boids.SessionState.TERMINATED: [
        boids_api.boids.SessionState.ARCHIVED
    ],
    boids_api.boids.SessionState.ARCHIVED: []
}

class PendingSessions:
    """
    Collection of Sessions which have been created (by user request) but have
    not yet been claimed by an Engine.
    """

    def __init__(self):
        self._items = []
        self._topic = boids_utils.pubsub.get_topic_publisher('boids.sessions')

    def __len__(self):
        return len(self._items)

    def append(self, item: boids_api.boids.SessionConfigurationStatus):
        """ Adds a 'pending' Session to the in-memory collection of PendingSessions """
        self._items.append(item)
        self._topic.publish(item.to_dict())
        LOGGER.info(f"Session '{item.uuid}' {item.state}")


async def search(title: str = None,
           state: boids_api.boids.SessionState = None,
           entity_id: str = None,
           pagination: boids_api.boids.Pagination = None) -> boids_api.boids.SessionConfigurationStatusList:
    """ Searches for one or more Sessions matching the given search criteria. """
    # pylint: disable-next=fixme
    # TODO: Exclude ARCHIVE unless explicitly requested
    data, pagination = boids_utils.elastic.indices.session_configuration.search(title=title,
                                                                                state=state,
                                                                                uuid=entity_id,
                                                                                pagination=pagination)

    return boids_api.boids.SessionConfigurationStatusList(values=data,
                                                         pagination=pagination)

async def create(config: boids_api.boids.SessionConfiguration,
           base_url: yarl.URL) -> boids_api.boids.SessionConfigurationStatus:
    """ Creates a Session """
    config = boids_utils.openapi.instance.expand_defaults(config, boids_api.boids.SessionConfiguration)
    session = boids_api.boids.SessionConfigurationStatus.from_dict(config.to_dict())

    session.uuid = boids_utils.mk_uuid()
    session.state = boids_api.boids.SessionState.PENDING
    session.url = str(base_url.joinpath(session.uuid))
    session.next_states = NEXT_STATES[session.state]
    session.created = boids_utils.nowutc(stringify=True)
    session.modified = session.created

    boids_utils.elastic.indices.session_configuration.save(session)
    await boids_utils.pubsub.get_topic_publisher(SESSIONS_TOPIC).publish(session.to_dict())

    return session

async def modify(entity_id: str,
           update: boids_api.boids.SessionConfiguration,
           base_url: yarl.URL) -> boids_api.boids.SessionConfigurationStatus:
    """ Updates a Session """
    existing = boids_utils.elastic.indices.session_configuration.get(entity_id)

    modified = boids_utils.openapi.merge_models(existing, update)
    modified.url = str(base_url.joinpath(existing.uuid))

    boids_utils.elastic.indices.session_configuration.save(modified)
    await boids_utils.pubsub.get_topic_publisher(SESSIONS_TOPIC).publish(modified.to_dict())

    return modified


async def get(entity_id: str) -> boids_api.boids.SessionConfigurationStatus:
    """
    Returns the identified Session.  Raises NoSuchDocument if no Session with
    the given UUID exists.
    """
    return boids_utils.elastic.indices.session_configuration.get(entity_id)
