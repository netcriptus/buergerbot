from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins='*')


def create_app(debug=False, **config_overrides):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)
    from web_app.blueprints import anmeldung
    app.register_blueprint(anmeldung)

    socketio.init_app(app)
    return app
