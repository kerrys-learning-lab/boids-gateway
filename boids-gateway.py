#! /usr/bin/env python3
''' Main executable for the boids-gateway application. '''
import argparse
import logging
import logging.config
import boids_utils.config
import boids_utils.elastic
import boids_utils.logging
import boids_utils.openapi
import boids_utils.pubsub
import boids

APP_NAME='boids-gateway'
LOGGER=logging.getLogger(APP_NAME)
DEFAULT_PORT=8888

# Order is important
# - utils.config *must* be first in order to load all configuration files
#   for subsequent stakeholders
# - utils.logging *should* be early in order to facilitate debugging
CLI_STAKEHOLDERS = [
    boids_utils.config,
    boids_utils.logging,
    boids_utils.openapi,
    boids_utils.elastic,
    boids_utils.pubsub
]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='BOIDS')

    server_group = parser.add_argument_group(title='Server options')
    server_group.add_argument('-p',
                              '--port',
                              default=DEFAULT_PORT,
                              help=f'Specify the server port.  Default: {DEFAULT_PORT}')

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.add_cli_options(parser)

    args = parser.parse_args()

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.process_cli_options(args, **boids_utils.config.instance)

    app = boids.create_app()
    app.run(port=args.port)
