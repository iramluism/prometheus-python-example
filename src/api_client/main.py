
import time
from fastapi import FastAPI, HTTPException, status
from starlette.requests import Request 

from prometheus_client import make_asgi_app, Counter, Histogram, Gauge


app = FastAPI()
counter = Counter("healthcheck", "Healthchecks")
http_requests = Gauge("http_requests", "Http Requests", ["method", "endpoint", "status_code"])
requests_counter = Counter("client_http_request", "Http Requests", ["method", "endpoint"])
http_responses = Histogram("http_responses", "Duration Time Request", ["method", "endpoint", "status_code"])


@app.get("/ready")
async def ready():
    #return "ok"
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/health")
async def health():
    counter.inc()
    return "OK"


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

    
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """ Captch Metric from api 
    Metrics:
        1. client_http_request
        2. duration_time_request
    """

    init_time = time.time()
    
    requests_counter.labels(request.method, request.url.path).inc()
    response = await call_next(request)
    print("endpoint: ", request.url.path)
    
    end_time = time.time()
    duration_time_request = end_time - init_time
    print("time: ", duration_time_request)
    print("status:", response.status_code)
    http_responses.labels(request.method, request.url.path, response.status_code).observe(duration_time_request)
    
    return response
