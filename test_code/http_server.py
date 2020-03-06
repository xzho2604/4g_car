from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


# receive command from http
@app.route('/', methods=['POST'])
def addOne():
    cmd = request.get_json()
    print("received:" , cmd)
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)
