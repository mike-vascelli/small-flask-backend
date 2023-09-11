from typing import List

from flask import make_response

from deserializers.request import Request
from models.model import Model


def created_response(model: Model):
    return make_response(model.to_dict(), 201)


def list_response(models: List[Model]):
    return make_response([m.to_dict() for m in models], 200)


def no_content_response():
    response = make_response("", 204)
    response.mimetype = "application/json"
    return response


def bad_request_response(request: Request):
    return make_response(request.error_details(), 400)


def unprocessable_response(e):
    return make_response(e.__dict__, 422)


def not_found_response(e):
    return make_response(e.__dict__, 404)


def method_not_allowed_response(e):
    return make_response(e.__dict__, 405)


def service_error_response(e):
    return make_response(e.__dict__, 500)
