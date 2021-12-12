from flask import Flask, jsonify, request
from core.users import UserManager
from werkzeug.exceptions import HTTPException
from schemas.user import UserRegistrationModel

app = Flask(__name__)

user_manager = UserManager("users.json")


@app.errorhandler(HTTPException)
def handle_auth_error(e: HTTPException):
    return jsonify({"error": e.description, "type": type(e).__name__}), e.code


@app.route("/")
def index():
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        username = "Unknown"
    else:
        username, password = auth_header.split(":", maxsplit=2)
        user_manager.authenticate(username, password)

    return jsonify({"msg": f"Hello, {username}!"})


@app.route("/user", methods=["POST"])
def register():
    data = UserRegistrationModel(**request.json)
    user_manager.create_user(data.username, data.password)

    return jsonify("info": "Success")


if __name__ == "__main__":
    app.run(debug=True)