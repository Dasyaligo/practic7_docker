from flask import Flask, jsonify, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_app_requests_total', 'Total request count', ['method', 'endpoint', 'status'])
ERROR_COUNT = Counter('flask_app_errors_total', 'Total errors')
ACTIVE_USERS = Gauge('flask_app_active_users', 'Number of active users')
RESPONSE_TIME = Histogram('flask_app_response_time_seconds', 'Response time')
CPU_USAGE = Gauge('flask_app_cpu_usage_percent', 'CPU usage percent')


@app.route('/')
def home():
    start_time = time.time()
    
    time.sleep(random.uniform(0.1, 0.5))
    is_error = random.choice([False, False, False, True])
    
    ACTIVE_USERS.inc()
    CPU_USAGE.set(random.uniform(10.0, 80.0))
    RESPONSE_TIME.observe(time.time() - start_time)
    
    if is_error:
        ERROR_COUNT.inc()
        REQUEST_COUNT.labels(method='GET', endpoint='/', status='500').inc()
        return jsonify(error="Internal Server Error"), 500
        
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    return jsonify(message="Hello, DevOps!")


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)