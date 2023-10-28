"""
Business-logic used by web-views for Session CRUD operations.
"""
import logging
import yarl
import boidsapi.model
import boids_utils
import boids_utils.elastic
import boids_utils.openapi
import boids_utils.pubsub

LOGGER = logging.getLogger('session')

SESSIONS_TOPIC = 'boids.sessions'

NEXT_STATES = {
    boidsapi.model.SessionState.PENDING: [],
    boidsapi.model.SessionState.PAUSED: [
      boidsapi.model.SessionState.RESET,
      boidsapi.model.SessionState.RUNNING,
      boidsapi.model.SessionState.STEP,
      boidsapi.model.SessionState.TERMINATED
    ],
    boidsapi.model.SessionState.RESET: [
      boidsapi.model.SessionState.RUNNING,
      boidsapi.model.SessionState.STEP,
      boidsapi.model.SessionState.TERMINATED,
      boidsapi.model.SessionState.ARCHIVED
    ],
    boidsapi.model.SessionState.RUNNING: [
      boidsapi.model.SessionState.PAUSED,
      boidsapi.model.SessionState.STEP,
      boidsapi.model.SessionState.TERMINATED
    ],
    boidsapi.model.SessionState.STEP: [
        boidsapi.model.SessionState.PAUSED,
        boidsapi.model.SessionState.RUNNING,
        boidsapi.model.SessionState.TERMINATED
    ],
    boidsapi.model.SessionState.TERMINATED: [
        boidsapi.model.SessionState.ARCHIVED
    ],
    boidsapi.model.SessionState.ARCHIVED: []
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

    def append(self, item: boidsapi.model.SessionConfigurationStatus):
        """ Adds a 'pending' Session to the in-memory collection of PendingSessions """
        self._items.append(item)
        self._topic.publish(item.to_dict())
        LOGGER.info(f"Session '{item.uuid}' {item.state}")


async def search(title: str = None,
           state: boidsapi.model.SessionState = None,
           entity_id: str = None,
           pagination: boidsapi.model.Pagination = None) -> boidsapi.model.SessionConfigurationStatusList:
    """ Searches for one or more Sessions matching the given search criteria. """
    # pylint: disable-next=fixme
    # TODO: Exclude ARCHIVE unless explicitly requested
    data, pagination = boids_utils.elastic.indices.session_configuration.search(title=title,
                                                                                state=state,
                                                                                uuid=entity_id,
                                                                                pagination=pagination)

    return boidsapi.model.SessionConfigurationStatusList(values=data,
                                                         pagination=pagination)

async def create(config: boidsapi.model.SessionConfiguration,
           base_url: yarl.URL) -> boidsapi.model.SessionConfigurationStatus:
    """ Creates a Session """
    config = boids_utils.openapi.instance.expand_defaults(config, boidsapi.model.SessionConfiguration)
    session = boidsapi.model.SessionConfigurationStatus.from_dict(config.to_dict())

    session.uuid = boids_utils.mk_uuid()
    session.state = boidsapi.model.SessionState.PENDING
    session.url = str(base_url.joinpath(session.uuid))
    session.next_states = NEXT_STATES[session.state]
    session.created = boids_utils.nowutc(stringify=True)
    session.modified = session.created

    boids_utils.elastic.indices.session_configuration.save(session)
    await boids_utils.pubsub.get_topic_publisher(SESSIONS_TOPIC).publish(session.to_dict())

    return session

async def modify(entity_id: str,
           update: boidsapi.model.SessionConfiguration,
           base_url: yarl.URL) -> boidsapi.model.SessionConfigurationStatus:
    """ Updates a Session """
    existing = boids_utils.elastic.indices.session_configuration.get(entity_id)

    modified = boids_utils.openapi.merge_models(existing, update)
    modified.url = str(base_url.joinpath(existing.uuid))

    boids_utils.elastic.indices.session_configuration.save(modified)
    await boids_utils.pubsub.get_topic_publisher(SESSIONS_TOPIC).publish(modified.to_dict())

    return modified


async def get(entity_id: str) -> boidsapi.model.SessionConfigurationStatus:
    """
    Returns the identified Session.  Raises NoSuchDocument if no Session with
    the given UUID exists.
    """
    return boids_utils.elastic.indices.session_configuration.get(entity_id)
