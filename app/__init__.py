from app.routes.{{.Route}} import {{.Route}}_blueprint
from app.health import health_blueprint
from app.external_services import services
from app.prometheus import register_metrics
from flask import Flask, jsonify, send_from_directory
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import requests
import os
import socket

os.system("npx openapi-comment-parser . app/swagger/openapi.json")

app = Flask(
    __name__,
    static_folder=os.path.join(os.getcwd(), "app/swagger"),
)

app.register_blueprint(health_blueprint)
app.register_blueprint({{.Route}}_blueprint, url_prefix="/api/v1/{{.Route}}")

register_metrics(app)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})


@app.route("/api-docs", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/info", methods=["GET"])
def info():
    info_list = []
    for service in services:
        try:
            res = requests.get("{}/info".format(services[service]), timeout=10)
            info_list.append(res.json())
        except Exception:
            continue

    return jsonify(
        {
            "service": os.environ["SERVICE"] if "SERVICE" in os.environ else "{{.ServiceNamePill}}",
            "hostname": socket.gethostname(),
            "database": None,
            "children": info_list,
            "language": "Python",
            "url": os.environ["{{.ServiceNameTitle}}_URL"]
            if "{{.ServiceNameTitle}}_URL" in os.environ
            else "http://localhost:{{.Port}}",
        }
    )
