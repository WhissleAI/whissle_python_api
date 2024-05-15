from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import configure_routes
    configure_routes(app)
    return app