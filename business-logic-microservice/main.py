import requests
from flask import Flask, request, Response, jsonify
app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    json_object = request.get_json(silent=True)
    if not json_object:
        return jsonify({"error": "JSON data is missing"}), 400

    # try to get all needed information from json
    try:
        username = json_object['username']
        password = json_object['password']

        if not username or not password:
            return jsonify({"error": "Username or password cannot be empty."}), 400

    except KeyError:
        # not all data received
        return jsonify({"error": "Please provide both username and password."}), 400
    
    response = requests.post("http://localhost:8888/api/auth/login", json=json_object)
    if response.status_code == 401:
        return jsonify({"error": "UNAUTHORIZED user"}), 401
    
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    
    tokens_json = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return jsonify(tokens_json), 200

def validate_tokens(json_object):
    if not json_object:
        return jsonify({"error": "JSON data is missing"}), 400
    
    try:
        access_token = json_object['access_token']
    except KeyError:
        return jsonify({"error": "Missing access token"}), 400
    
    json_access_token = {
        "access_token":access_token
    }
    response = requests.post("http://localhost:8888/api/auth/validate", json=json_access_token)
    
    if response.json()['active'] == False:
        print("SUCAAa")
        try:
            refresh_token = json_object['refresh_token']
        except KeyError:
            return jsonify({"error":"You are logged out, please log in again"}), 400
        
        json_refresh_token = {
            "refresh_token":refresh_token
        }

        response = requests.post("http://localhost:8888/api/auth/refresh", json=json_refresh_token)
        if response.status_code == 400:
            return jsonify({"error":"Bad refresh token"}), 400
        
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']

        return jsonify({"access_token":access_token, "refresh_token":refresh_token}), 200
        
    return None, 200

def generic_response(url, ok_status,methods):
    json_object = request.get_json(silent=True)
    validation_response, status_code = validate_tokens(json_object)
    if status_code == 400:
        return validation_response, 400
    if status_code == 200:
        if methods == "POST":
            response = requests.post(url,json=json_object)
        if methods == "GET":
            response = requests.get(url)
        if methods == "PUT":
            response = requests.put(url, json=json_object)
        if methods == "DELETE":
            response = requests.delete(url)

        if response.status_code != ok_status:
            return jsonify(response.json()), response.status_code
        else:
            if validation_response is not None:
                response_json = {
                    "access_token" : validation_response.get_json()['access_token'],
                    "refresh_token" : validation_response.get_json()['refresh_token']
                }
                if methods not in ["PUT", "DELETE"]:
                    response_json["response"] = response.json()
                # print(response_json)
                return jsonify(response_json), ok_status
            else:
                return jsonify(response.json()), response.status_code

    return Response(status=ok_status)

#=================

@app.route("/countries", methods=["POST"])
def post_country():
    return generic_response("http://localhost:6000/api/countries", 201, "POST")

@app.route("/countries", methods=["GET"])
def get_country():
    return generic_response("http://localhost:6000/api/countries", 200, "GET")

@app.route("/countries", methods=["PUT"])
def put_country():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_country_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/countries/" + str(check_country_id)

    return generic_response(url, 200, "PUT")

@app.route("/countries", methods=["DELETE"])
def delete_country():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_country_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/countries/" + str(check_country_id)

    return generic_response(url, 200, "DELETE")

#====================

@app.route("/city", methods=["POST"])
def post_city():
    return generic_response("http://localhost:6000/api/cities", 201, "POST")

@app.route("/city", methods=["GET"])
def get_city():
    return generic_response("http://localhost:6000/api/cities", 200, "GET")

@app.route("/city", methods=["PUT"])
def put_city():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_city_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/cities/" + str(check_city_id)

    return generic_response(url, 200, "PUT")

@app.route("/city", methods=["DELETE"])
def delete_city():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_city_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/cities/" + str(check_city_id)

    return generic_response(url, 200, "DELETE")


#====================

@app.route("/temperatures", methods=["POST"])
def post_temperatures():
    return generic_response("http://localhost:6000/api/temperatures", 201, "POST")

@app.route("/temperatures", methods=["GET"])
def get_temperatures():
    return generic_response("http://localhost:6000/api/temperatures", 200, "GET")

@app.route("/temperatures", methods=["PUT"])
def put_temperatures():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_temperatures_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/temperatures/" + str(check_temperatures_id)

    return generic_response(url, 200, "PUT")

@app.route("/temperatures", methods=["DELETE"])
def delete_temperatures():
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)
    try:
        check_temperatures_id = json_object['id']
    except KeyError:
        return Response(status=400)

    url = "http://localhost:6000/api/temperatures/" + str(check_temperatures_id)

    return generic_response(url, 200, "DELETE")

@app.route("/city/country", methods=["GET"])
def get_city_by_country():
    return jsonify({"erorr":"Not yet impemented"}) , 200

@app.route("/temperatures/cities", methods=["GET"])
def get_temperature_by_city():
    return jsonify({"erorr":"Not yet impemented"}) , 200

@app.route("/temperatures/country", methods=["GET"])
def get_temperature_by_country():
    return jsonify({"erorr":"Not yet impemented"}) , 200

if __name__ == "__main__":
    app.run()