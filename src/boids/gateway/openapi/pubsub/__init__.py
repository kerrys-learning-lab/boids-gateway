"""
Web-view for sessions.

The classes and methods here are dummies, since we represent pubsub topics using
the OpenAPI spec, but pubsub features are not implemented using HTTP.

TODO: Convert these features to AsyncAPI vice OpenAPI.
"""

class SessionsView:
    """
    Web-view for session-related events.
    """

    async def get(self):
        """
        Represents an event-stream of SessionConfiguration updates
        """
        raise RuntimeError('not implemented')

    async def search(self):
        """
        Required by connexion
        """
        raise RuntimeError('not implemented')
