from app.services import data_handler
from app.errors import example_error
from app.jaeger import Jaeger
from flask import jsonify, request, Blueprint
from datetime import datetime
from pybreaker import CircuitBreaker

{{.Route}}_blueprint = Blueprint("{{.Route}}_blueprint", __name__)

breaker = CircuitBreaker(fail_max=5, reset_timeout=30)

context = Jaeger()


@{{.Route}}_blueprint.route("/", methods=["GET"])
def {{.Route}}():
    """
    /**
    * GET /api/v1/{{.Route}}
    * @description Example route
    * @response 200 - OK
    * @response 400 - Error
    */
    """

    context.start("{{.Route}}", request)
    try:
        data = breaker.call(data_handler.get_data, context)
        status_code = 200
    except Exception as e:
        data = {"error": e.args[0]}
        status_code = 400
    finally:
        context.stop(status_code)
        return jsonify(data), status_code
