from flask import Flask, request, jsonify,  render_template
import requests

app = Flask(__name__)

# Pong service URL
PONG_SERVICE_URL = "http://pong.app.kind.org:31080/pong"  # Replace <pong-service-url> with the actual Pong service URL


# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')


# Ping endpoint
@app.route('/ping', methods=['POST'])
def ping():
    data = request.get_json()
    player_name = data.get('playerName')

    if not player_name:
        return jsonify({'message': 'Player name is required'}), 400

    # Call the pong service
    pong_response = requests.post(PONG_SERVICE_URL, json={'playerName': player_name})

    if pong_response.status_code != 200:
        return jsonify({'message': 'Error from pong service'}), pong_response.status_code

    return jsonify(pong_response.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
