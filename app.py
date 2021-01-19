from flask import Flask, jsonify
from helpers.data import Data

api = Flask(__name__)

@api.route('/player/stats/<id>', methods=['GET'])
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
    api.run(debug=True)