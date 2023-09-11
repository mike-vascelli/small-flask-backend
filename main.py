from flask import Flask

from controllers import algorithms_routes, root_routes

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask('algorithm_app')
app.register_blueprint(algorithms_routes.algorithms_blueprint)
app.register_blueprint(root_routes.root_blueprint)
app.run(host="0.0.0.0", port=8080)
