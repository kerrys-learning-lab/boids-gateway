""" Defines async HTTP CRUD operations for Boids """

class BoidView:
    """ Defines async HTTP CRUD operations for Boids """

    def search(self):
        """
        Searches for Boids matching the given search criteria.
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
        """ Returns the Boid identified by the given UUID """

    def post(self):
        """ Creates a new Boid """

    def put(self):
        """ Modifies an existing Boid """

    def delete(self):
        """ Deletes a Session """
