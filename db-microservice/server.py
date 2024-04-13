from flask import Flask, request, Response
from datetime import datetime
import psycopg
import json
import collections

from psycopg.errors import UniqueViolation, ForeignKeyViolation, IntegrityConstraintViolation

connection = psycopg.connect("dbname=db_idp user=idp_user password=idp_pass host=idp_postgres port=5432")
cursor = connection.cursor()
app = Flask(__name__)

# Create database if database does not exist
cursor.execute("""
create table if not exists "Tari"
(
    id integer generated always as identity
        constraint id_pk
            primary key,
    nume_tara varchar
        constraint nume_tara_pk
            unique,
    latitudine  double precision,
    longitudine double precision
);

alter table "Tari"
    owner to tema2;

create table if not exists "Orase"
(
    id integer generated always as identity
        constraint "id_Cities_pk"
            primary key,
    id_tara integer
        constraint "idTaraCities_idCountries__fk"
            references "Tari",
    nume_oras varchar,
    latitudine double precision,
    longitudine double precision,
    constraint "idtara_numeOras_pk"
        unique (nume_oras, id_tara)
);

alter table "Orase"
    owner to tema2;

create table if not exists "Temperaturi"
(
    id_oras integer
        constraint "idOrasTemperaturi_idOras__fk"
            references "Orase",
    valoare double precision,
    timestamp timestamp,
    id integer generated always as identity
        constraint id_temperaturi_pk
            primary key,
    constraint "idOras_timestamp_pk"
        unique (id_oras, timestamp)
);

alter table "Temperaturi"
    owner to tema2;

""")
connection.commit()


@app.route("/api/countries", methods=["POST"])
def post_country():
    global cursor
    global connection

    # Get JSON from body
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)

    # try to get all needed information from json
    try:
        country_name = json_object['nume']
        country_lon = json_object['lon']
        country_lat = json_object['lat']
    except KeyError:
        # not all data received
        return Response(status=400)

    insert_command_in_country_table = """
    insert into "Tari" (nume_tara, latitudine, longitudine)
    values ('{tara}', {latitudine}, {longitudine});
    """

    # Request to add in table
    try:
        cursor.execute(insert_command_in_country_table.format(tara=country_name, latitudine=country_lat,
                                                              longitudine=country_lon))
        connection.commit()
    except UniqueViolation:
        connection.rollback()
        return Response(status=409)
    except ForeignKeyViolation:
        connection.rollback()
        return Response(status=409)
    except IntegrityConstraintViolation:
        connection.rollback()
        return Response(status=409)
    except Exception:
        connection.rollback()
        return Response(status=409)

    request_country_id = """select id from "Tari" where nume_tara='{nume_tara}';"""
    try:
        cursor.execute(request_country_id.format(nume_tara=country_name))
    except Exception:
        # If there is a problem with the id fetch, it means that something went wrong
        connection.rollback()
        return Response(status=500)

    # get created country id to return
    created_id = cursor.fetchall()
    country_id = created_id.pop()
    return Response(json.dumps({"id": country_id[0]}, indent=4), status=201, mimetype="application/json")


@app.route("/api/countries", methods=["GET"])
def get_country():
    global cursor
    global connection

    request_all_countries = """select id, nume_tara, latitudine, longitudine from "Tari";"""
    try:
        cursor.execute(request_all_countries)
    except Exception:
        # If there is a problem with the country fetch, it means that something went wrong
        connection.rollback()
        return Response(status=500)

    all_countries = cursor.fetchall()

    # generate return list
    return_list = []
    for country in all_countries:
        country_dict = collections.OrderedDict(
            {"id": country[0], "nume": country[1], "lat": country[2], "lon": country[3]})
        return_list.append(country_dict)
    return Response(json.dumps(return_list, indent=4), status=200, mimetype="application/json")


@app.route("/api/countries/<int:country_id>", methods=["PUT"])
def put_country(country_id):
    global cursor
    global connection

    # get json body
    json_object = request.get_json(silent=True)
    if not json_object:
        return Response(status=400)

    try:
        check_country_id = json_object['id']
        country_name = json_object['nume']
        country_lon = json_object['lon']
        country_lat = json_object['lat']
    except KeyError:
        return Response(status=400)

    # this JSON is not for this request
    if not (check_country_id == country_id):
        return Response(status=400)

    update_country_request = """
    update "Tari"
    set latitudine = {latitudine},
        longitudine = {longitudine},
        nume_tara = '{nume_tara}'
    where id = {id};
    """
    try:
        cursor.execute(
            update_country_request.format(latitudine=country_lat, longitudine=country_lon, nume_tara=country_name,
                                          id=country_id))
        connection.commit()
    except UniqueViolation:
        connection.rollback()
        return Response(status=409)
    except ForeignKeyViolation:
        connection.rollback()
        return Response(status=409)
    except Exception:
        connection.rollback()
        return Response(status=500)

    return Response(status=200)


@app.route("/api/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):
    global cursor
    global connection

    delete_country_request = """
    delete
    from "Tari"
    where id = {id};
    """
    try:
        cursor.execute(delete_country_request.format(id=country_id))
        connection.commit()
    except Exception:
        connection.rollback()
        return Response(status=404)

    return Response(status=200)


@app.route("/api/cities", methods=["POST"])
def post_city():
    pass

@app.route("/api/cities", methods=["GET"])
def get_cities():
    pass

@app.route("/api/cities/country/<int:country_id>", methods=["GET"])
def get_city_by_country(country_id):
    pass

@app.route("/api/cities/<int:city_id>", methods=["PUT"])
def put_city(city_id):
    pass

@app.route("/api/cities/<int:city_id>", methods=["DELETE"])
def delete_city(city_id):
    pass

@app.route("/api/temperatures", methods=["POST"])
def post_temperatures():
    pass

@app.route("/api/temperatures", methods=["GET"])
def get_temperatures():
    pass

@app.route("/api/temperatures/cities/<int:city_id>", methods=["GET"])
def get_temperature_by_city(city_id):
    pass

@app.route("/api/temperatures/countries/<int:country_id>", methods=["GET"])
def get_temperature_by_country(country_id):
    pass

@app.route("/api/temperatures/<int:temperature_id>", methods=["PUT"])
def put_temperature(temperature_id):
    pass

@app.route("/api/temperatures/<int:temperature_id>", methods=["DELETE"])
def delete_temperature(temperature_id):
   pass

if __name__ == "__main__":
    app.run()
