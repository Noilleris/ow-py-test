from flask import Flask, jsonify

from src.dataStructure.messages import Messages
from src.dataStructure.usage import Usage

from src.helpers.api import current_period
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/usage', methods=['GET'])
def usage():
    period_data = current_period()
    res = Usage(Messages(period_data).messages)
    return jsonify(res.to_dict())