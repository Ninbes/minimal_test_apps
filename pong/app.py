from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import socket
import redis

app = Flask(__name__)
CORS(app)
#CORS added
# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', '')

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


@app.route('/pong', methods=['POST'])
def pong():
    data = request.get_json()
    player_name = data.get('playerName')

    if not player_name:
        return jsonify({'message': 'Player name is required'}), 400

    # Increment the counter in Redis with a 1-minute TTL
    key = f"ping_count:{player_name}"
    r.incr(key)
    r.expire(key, 60)
    ping_count = r.get(key)

    # Get the pod name
    pod_name = socket.gethostname()

    response = {
        'playerName': player_name,
        'podName': pod_name,
        'pingCount': int(ping_count)
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
