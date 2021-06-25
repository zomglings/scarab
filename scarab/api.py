from bugout.app import Bugout
from bugout.data import BugoutUser
from flask import Flask, render_template, request, Request

app = Flask(__name__)

bugout_client = Bugout()

class AuthenticationError(Exception):
    """
    Raised when there was an error authenticating a user for whatever reason.
    """
    pass

def get_token(req: Request) -> BugoutUser:
    authorization_value = req.headers["Authorization"]
    authorization_prefix = "Bearer "
    if not authorization_value.startswith(authorization_prefix):
        raise AuthenticationError(f"Invalid Authorization header - should start with \"{authorization_prefix}\"")
    token = authorization_value[len(authorization_prefix):]
    return token

@app.route("/ping")
def ping():
	return {"status": "ok"}

@app.route("/login")
def login():
    return render_template("login.html", subtitle="Login")

@app.route("/user", methods=["POST"])
def user():
    username = request.form["username"]
    password = request.form["password"]
    response = bugout_client.create_token(username=username, password=password)
    token = response.id
    user = bugout_client.get_user(token)
    return {"token": token, "user": user.json()}

@app.route("/logout", methods=["POST"])
def logout():
    token = get_token(request)
    bugout_client.revoke_token(token=token)
    return {"token": token, "status": "revoked"}

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    user = bugout_client.create_user(username=username, email=email, password=password)
    return user.json()
