""" Defines async HTTP CRUD operations for Events """
class EventView:
    """ Defines async HTTP CRUD operations for Events """

    def search(self):
        """
        Searches for Events matching the given search criteria.
        """
        # pagination = self.get_pagination()
        # results = self.elasticsearch.search(index="boids.sessions",
        #                                     from_=pagination.offset,
        #                                     size=pagination.limit,
        #                                     sort=self.elasticsearch.to_sort(pagination),
        #                                     query=Elasticsearch._extract_search(search))
        # return Elasticsearch._extract_results('SEARCH boids.sessions', results)
        raise RuntimeError('not implemented')

    def get(self):
        """ Returns the Event identified by the given UUID """

    def post(self):
        """ Creates a new Event """

    def put(self):
        """ Modifies an existing Event """

    def delete(self):
        """ Deletes an Event """
