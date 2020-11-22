from flask import Flask, render_template, jsonify, request
from pathfinding import calculate_path

app = Flask(__name__)

@app.route('/')
def main_page():

    return render_template("landing.html")



@app.route('/_algorithm')
def main_page_request():
    #print(request.query_string)
    alg_type = request.args.get('type')
    data = request.args.get('data')
    response = calculate_path(alg_type, data)

    return jsonify(response)


if __name__ == "__main__":
    # http://127.0.0.1:5000/
    # set FLASK_ENV=development
    # flask run
    app.run(debug=False)