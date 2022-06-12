# uwsgi --master --https localhost:5683,server-public-key.pem,server-private-key.pem --mount /=server:app

from flask import Flask

SECRET_MESSAGE = "fluffy tail"
app = Flask(__name__)

@app.route("/")
def get_secret_message():
    return SECRET_MESSAGE