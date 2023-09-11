from flask import Blueprint

from serializers.responses import method_not_allowed_response

root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
def root():
    return "Algorithm System is up and running"


@root_blueprint.app_errorhandler(405)
def method_not_allowed(e):
    return method_not_allowed_response(e)
