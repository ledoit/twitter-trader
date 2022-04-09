# Created by Phil Ledoit

from flask import *

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
