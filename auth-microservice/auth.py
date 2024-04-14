from keycloak import KeycloakAdmin
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError
from flask import Flask, request, Response
import json

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://idp-keycloak:8080/",
                                 client_id="idp-confidential",
                                 realm_name="master",
                                 client_secret_key="jhFe0aOU179oNRk1vXRXfGgjQC1469k7")

admin = KeycloakAdmin(
    server_url="http://idp-keycloak:8080/",
    username='admin',
    password='admin',
    realm_name="master")

app = Flask(__name__)


@app.route("/api/auth/login", methods=["POST"])
def login_user():
    global keycloak_openid
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)

    # try to get all needed information from json
    try:
        username = json_object['username']
        password = json_object['password']
    except KeyError:
        # not all data received
        return Response(status=400)

    try:
        token = keycloak_openid.token(username, password)
    except KeycloakAuthenticationError as e:
        return Response(status=401)
    return Response(json.dumps(token) , status=200)


@app.route("/api/auth/logout", methods=["GET"])
def logout_user():
    global keycloak_openid
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
        # try to get all needed information from json
    try:
        refresh_token = json_object['refresh_token']
    except KeyError:
        # not all data received
        return Response(status=400)

    try:
        keycloak_openid.logout(refresh_token)
    except KeycloakPostError as e:
        return Response(status=400)
    return Response(status=200)


@app.route("/api/auth/register", methods=["POST"])
def register_user():
    global admin
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        new_user = admin.create_user(json_object)
    except KeycloakPostError as e:
        return Response(status=409)
    return Response(json.dumps(new_user), status=201)


@app.route("/api/auth/validate", methods=["POST"])
def validate_token():
    global keycloak_openid
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        access_token = json_object['access_token']
    except KeyError:
        # not all data received
        return Response(status=400)
    token_info = keycloak_openid.introspect(access_token)
    return Response(json.dumps(token_info), status=200)


@app.route("/api/auth/refresh", methods=["POST"])
def get_new_token():
    global keycloak_openid
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        refresh_token = json_object['refresh_token']
    except KeyError:
        # not all data received
        return Response(status=400)
    try:
        token = keycloak_openid.refresh_token(refresh_token)
    except KeycloakPostError as e:
        return Response(status=400)
    return Response(json.dumps(token), status=201)

if __name__ == "__main__":
    app.run()
