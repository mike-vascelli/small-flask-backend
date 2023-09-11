from flask import Blueprint, current_app, request

from deserializers.creation_request import CreationRequest
from deserializers.update_request import UpdateRequest
from repositories.in_memory_repository import InMemoryRepository
from repositories.repository import RepositoryClientError, RecordNotFound
from serializers.responses import created_response, unprocessable_response, not_found_response, service_error_response, \
    bad_request_response, no_content_response, list_response
from services.algorithms_service import AlgorithmsService

URL_PREFIX = "/api/v1/algorithms"

algorithms_blueprint = Blueprint(
    "algorithms", import_name=__name__, url_prefix=URL_PREFIX
)

algorithms_repository = InMemoryRepository()
algorithms_service = AlgorithmsService(algorithms_repository)


@algorithms_blueprint.route("/", methods=["POST"])
def create():
    try:
        request_data = CreationRequest(request.data)
        if not request_data.is_valid():
            return bad_request_response(request_data)

        algorithm = algorithms_service.create(**request_data.validated_data())
        return created_response(algorithm)
    except RepositoryClientError as e:
        return unprocessable_response(e)
    except Exception as e:
        current_app.logger.error(f"Unexpected error on algorithm creation. Error={repr(e)}", e)
        return service_error_response(e)


@algorithms_blueprint.route("/<algorithm_pk>", methods=["PATCH"])
def update(algorithm_pk):
    try:
        request_data = UpdateRequest(request.data, pk=algorithm_pk)
        if not request_data.is_valid():
            return bad_request_response(request_data)

        algorithms_service.update(**request_data.validated_data())
        return no_content_response()
    except RecordNotFound as e:
        return not_found_response(e)
    except RepositoryClientError as e:
        return unprocessable_response(e)
    except Exception as e:
        current_app.logger.error(f"Unexpected error on algorithm update. Error={repr(e)}", e)
        return service_error_response(e)


@algorithms_blueprint.route("/", methods=["GET"])
def retrieve_all():
    try:
        return list_response(algorithms_service.retrieve_all())
    except Exception as e:
        current_app.logger.error(f"Unexpected error on algorithms retrieval. Error={repr(e)}", e)
        return service_error_response(e)
