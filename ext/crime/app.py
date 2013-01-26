from flask import Flask
app = Flask(__name__)

@app.route("/data/crime/<latitude>/<longitude>/")
def get_data():
    return "HI"

if __name__ == "__main__":
    app.run()