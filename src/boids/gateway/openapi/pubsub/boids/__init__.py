"""
Web-views for Boids, SystemTime, SystemEvents.

The classes and methods here are dummies, since we represent pubsub topics using
the OpenAPI spec, but pubsub features are not implemented using HTTP.

TODO: Convert these features to AsyncAPI vice OpenAPI.
"""

class BoidsView:
    """
    Web-view for Boids-related events.
    """

    def get(self):
        """
        Represents an event-stream of Boids updates
        """
        raise RuntimeError('not implemented')

    async def search(self):
        """
        Required by connexion
        """
        raise RuntimeError('not implemented')



class SystemTimeView:
    """
    Web-view for SystemTime-related events.
    """

    def get(self):
        """
        Represents an event-stream of SystemTime updates
        """
        raise RuntimeError('not implemented')

    async def search(self):
        """
        Required by connexion
        """
        raise RuntimeError('not implemented')


class SystemEventsView:
    """
    Web-view for SystemEvent-related messages.
    """

    def get(self):
        """
        Represents an event-stream of SystemEvent updates
        """
        raise RuntimeError('not implemented')

    async def search(self):
        """
        Required by connexion
        """
        raise RuntimeError('not implemented')
