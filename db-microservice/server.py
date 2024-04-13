from flask import Flask, request, Response
from datetime import datetime
import psycopg
import json
import collections

from psycopg.errors import UniqueViolation, ForeignKeyViolation, IntegrityConstraintViolation

connection = psycopg.connect("dbname=db_idp user=idp_user password=idp_pass host=localhost port=5432")
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
    pass

@app.route("/api/countries", methods=["GET"])
def get_country():
    pass

@app.route("/api/countries/<int:country_id>", methods=["PUT"])
def put_country(country_id):
    pass

@app.route("/api/countries/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):
    pass

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
