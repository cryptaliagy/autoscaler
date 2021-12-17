import subprocess

from typing import (
    Optional,
)

from flask import (
    Flask
)

from autoscaler.routes import webhook_route


def create_app(config_path: Optional[str] = None):
    '''
    Flask app factory function
    '''

    app = Flask(__name__)

    if config_path is not None:
        app.config.from_object(config_path)
    else:
        app.config.from_object('autoscaler.conf.EnvironmentConf')

    app.register_blueprint(webhook_route)

    subprocess.check_call(
        [
            'docker-compose',
            '-f',
            'devstack/runner.yaml',
            'build'
        ]
    )

    return app
