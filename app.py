from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("landing.html")


if __name__ == "__main__":
    # http://127.0.0.1:5000/
    app.run(debug=False)