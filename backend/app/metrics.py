"""Prometheus metrics."""
from prometheus_client import Counter, Histogram, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from flask import request, Response
import time

registry = CollectorRegistry(auto_describe=True)

REQUEST_COUNT = Counter(
    "opsportal_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
    registry=registry,
)
REQUEST_LATENCY = Histogram(
    "opsportal_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    registry=registry,
)


def _start_timer():
    request._start_time = time.perf_counter()


def _record(response):
    try:
        elapsed = time.perf_counter() - getattr(request, "_start_time", time.perf_counter())
        endpoint = request.endpoint or "unknown"
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, endpoint).observe(elapsed)
    except Exception:
        pass
    return response


def init_metrics(app):
    app.before_request(_start_timer)
    app.after_request(_record)


def metrics_response() -> Response:
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
