from flask import Flask, jsonify
from helpers.data import Data

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/player/stats/<id>', methods=['GET'])
def get_player_stats(id):
    try:
        player = Data.build_player_stats(id)
        return jsonify({
            'success': True,
            'data': player
        })
    except:
        return jsonify({
            'success': False,
            'message': 'API error'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')