from flask import Flask, request, json, Response
from dto.word_list_resp import WordListResp
from service.boggle_solver_service import findAllWords

app = Flask(__name__)

json_header = {'content-type': 'application/json'}

http_status = {'OK': 200, 'BAD_REQUEST': 400, 'ERROR': 500}

default_messages = {200: 'Successfully retrieved data', 400: 'Failed to retrieve data', 500: 'Error occurred while processing request'}

@app.route('/solve', methods=['GET'])
def solve_board():
    board = request.args.get('board')
    size = request.args.get('size')    

    try:
        if (board == None or size == None):
            return json_resp('Parameters board and size are required', [], http_status['BAD_REQUEST'])
        else:
            board = board.split(',')
            if (len(board) < size**2):
                return json_resp('Parameter board must be the size of the size parameter squared', [], http_status['BAD_REQUEST'])

        result = findAllWords(board)
        status = http_status['OK']
    except Exception:
        result = []
        status = http_status['ERROR']

    return json_resp(None, result, status)


def json_resp(message, payload = [], status=200):
    return (json.dumps(map_resp(message, payload, status)), status, json_header)

def map_resp(message, data = [], status=200):
    return WordListResp(len(data), data, status == http_status['OK'], message if message != None else default_messages[status]).serialize()
