""" Creates the Connextion web app """
import connexion
import connexion.resolver
import boids_utils.openapi

def create_app():
    """ Creates the Connextion web app """
    app = connexion.AioHttpApp(__name__,
                               specification_dir=boids_utils.openapi.instance.dirname)
    app.add_api(boids_utils.openapi.instance.basename,
                arguments={'title': boids_utils.openapi.instance.title},
                options={'swagger_ui': False},
                pythonic_params=True,
                pass_context_arg_name='request',
                resolver=connexion.resolver.MethodViewResolver('boids.gateway.openapi'))

    return app
