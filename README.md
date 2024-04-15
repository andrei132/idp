# Echipa Byte Crusaders Proiect IDP

## Descriere
Scopul acestui proiect este crearea unei aplicatii bazata pe microservici care va ajuta la monitorizarea de temperaturi in diferite orase-tari.

Aplicația de Monitorizare a Temperaturilor Globale este un sistem avansat care oferă utilizatorilor o platformă interactivă pentru a accesa, actualiza și analiza datele despre temperaturile din diferite orașe și țări. Scopul principal al aplicației este de a facilita monitorizarea schimbărilor climatice și de a oferi o sursă de informații fiabilă pentru publicul larg interesat de tendințele meteorologice globale

In final va trebui sa avem o aplicatie care respecta urmatoarele conditi

- [X] existența și integrarea celor minim 3 servicii proprii (0.9p)
    - [X] Serviciu de autentificare
    - [X] Serviciu de interactiune cu baza de date 
    - [X] Serviciu de bussines logic
- [X] existența și integrarea unui serviciu de baze de date (0.3p)
- [X] existența și integrarea unui serviciu de utilitar DB (0.3p)
- [X] existența și integrarea Portainer sau a unui serviciu similar (0.5p)
- [ ] utilizarea Docker și rularea într-un cluster Docker Swarm (0.6p)
  - [X] Utilizarea docker compose
  - [ ] Utilizarea docker swarm
- [X] existența și integrarea Kong sau a unui serviciu similar (0.6p)
- [X] existența și integrarea unui sistem de logging sau monitorizare, cu dashboard pentru observabilitate (0.5p)
- [X] utilizarea de Gitlab CI/CD (sau o unealtă similară) (0.3p)

## Done
La moment este implementat serviciul de autentificare cu ajutorul la keycloak, care este adaugat in compose.yaml
```yaml
  keycloak:
    container_name: idp-keycloak
    image: quay.io/keycloak/keycloak:23.0.1
    restart: always
    ports:
      - 8090:8080
    environment:
      KEYCLOAK_ADMIN: 'admin'
      KEYCLOAK_ADMIN_PASSWORD: 'admin'
    command:
      - start-dev
    volumes:
      - ./container-data/keycloak:/opt/keycloak/data/h2
    networks:
      - pythonapi
      - adminernet
```
Apoi cu ajutorul unei biblioteci pentru python a fost facut un wrapper peste keyclaok pentru a usura folosirea keycloak din cli, asa cum aplicatia nu e gandita sa contina UI
```python
@app.route("/api/auth/login", methods=["POST"])
@app.route("/api/auth/logout", methods=["GET"])
@app.route("/api/auth/register", methods=["POST"])
@app.route("/api/auth/validate", methods=["POST"])
@app.route("/api/auth/refresh", methods=["POST"])
```

Este adaugata o baza de date postgres cu date persistente la care se conecteaza db-microservice, scopul lui e interactiunea cu db
```yaml
postgres:
    container_name: idp_postgres
    image: postgres
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - pythonapi
      - adminernet
    environment:
      POSTGRES_USER: 'idp_user'
      POSTGRES_PASSWORD: 'idp_pass'
      POSTGRES_DB: 'db_idp'
```
Si un adminer care sa ajute la vizualizarea si modificarile bazei de date
```yaml
  adminer:
    container_name: idp-adminer
    image: adminer
    restart: always
    ports:
      - 8080:8080
    depends_on: 
      postgres:
        condition: service_healthy
    networks:
      - adminernet
```

De asemenea am adaugat portainer, pentru managementul containerelor
```yaml
  portainer:
      image: portainer/portainer-ce:latest
      ports:
        - 9443:9443
      volumes:
          - ./container-data/portainer:/data
          - /var/run/docker.sock:/var/run/docker.sock
      restart: unless-stopped
```

Api-ul care permite interactiunea cu data base-ul este microserviciul care se afla in db-microservice, acest microserviciu suporta urmatoarele requesturi
```python
@app.route("/api/countries", methods=["POST"])
@app.route("/api/countries", methods=["GET"])
@app.route("/api/countries/<int:country_id>", methods=["PUT"])
@app.route("/api/countries/<int:country_id>", methods=["DELETE"])
@app.route("/api/cities", methods=["POST"])
@app.route("/api/cities", methods=["GET"])
@app.route("/api/cities/country/<int:country_id>", methods=["GET"])
@app.route("/api/cities/<int:city_id>", methods=["PUT"])
@app.route("/api/cities/<int:city_id>", methods=["DELETE"])
@app.route("/api/temperatures", methods=["POST"])
@app.route("/api/temperatures", methods=["GET"])
@app.route("/api/temperatures/cities/<int:city_id>", methods=["GET"])
@app.route("/api/temperatures/countries/<int:country_id>", methods=["GET"])
@app.route("/api/temperatures/<int:temperature_id>", methods=["PUT"])
@app.route("/api/temperatures/<int:temperature_id>", methods=["DELETE"])
```

Asa cum in viitor va trebui sa adaugam docker swarm inseamna ca trebuie sa renuntam la build in docker compose, de accea avem nevoie sa publicam imaginile noastre pe dockerhub, pentru a nu face asta manual, au fost adaugate git actions(pipeline) care face build automat si il incarca pe dockerhub.

## Servicii proprii 
Serviciu de autentificare suporta uramtoarele endpoint-uri
```python
@app.route("/api/auth/login", methods=["POST"])
@app.route("/api/auth/logout", methods=["GET"])
@app.route("/api/auth/register", methods=["POST"])
@app.route("/api/auth/validate", methods=["POST"])
@app.route("/api/auth/refresh", methods=["POST"])
```
Aceste endpoint-uri nu sunt destinate pentru a fi apelate direct de catre utilizator

Serviciul de interactiune cu baza de date are urmatoarele endpoint-uri
```python
@app.route("/api/countries", methods=["POST"])
@app.route("/api/countries", methods=["GET"])
@app.route("/api/countries/<int:country_id>", methods=["PUT"])
@app.route("/api/countries/<int:country_id>", methods=["DELETE"])
@app.route("/api/cities", methods=["POST"])
@app.route("/api/cities", methods=["GET"])
@app.route("/api/cities/country/<int:country_id>", methods=["GET"])
@app.route("/api/cities/<int:city_id>", methods=["PUT"])
@app.route("/api/cities/<int:city_id>", methods=["DELETE"])
@app.route("/api/temperatures", methods=["POST"])
@app.route("/api/temperatures", methods=["GET"])
@app.route("/api/temperatures/cities/<int:city_id>", methods=["GET"])
@app.route("/api/temperatures/countries/<int:country_id>", methods=["GET"])
@app.route("/api/temperatures/<int:temperature_id>", methods=["PUT"])
@app.route("/api/temperatures/<int:temperature_id>", methods=["DELETE"])
```
Aceste endpoint-uri nu sunt destinate de a fi apelate de catre utilizator

Servicui de bussiness logic are urmatoarele endpointuri
```python
@app.route("/login", methods=["POST"])
@app.route("/countries", methods=["POST"])
@app.route("/countries", methods=["DELETE"])
@app.route("/city", methods=["POST"])
@app.route("/city", methods=["DELETE"])
@app.route("/temperatures", methods=["POST"])
@app.route("/temperatures", methods=["DELETE"])
@app.route("/city/country", methods=["GET"])
@app.route("/temperatures/cities", methods=["GET"])
@app.route("/temperatures/country", methods=["GET"])
```
Desi acest serviciu a fost alcatuit sa fie apelat de utilizator, cu ajutorul lui kong ne permitem sa pastram alte endpointuri, sau in caz ca decidem sa le modifcam in viitor, pentru utilizaotor nu e o problema

## Baze de date
Ca si baza de date a fost ales postgres, fiind usor de integrat in python
```yml
  postgres:
    container_name: idp_postgres
    image: postgres
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - pythonapi
      - adminernet
    environment:
      POSTGRES_USER: 'idp_user'
      POSTGRES_PASSWORD: 'idp_pass'
      POSTGRES_DB: 'db_idp'
```

## Utilitar DB
Ca si utilitar DB a fost ales adminer care permite administarea bazelor de date, intre care se gaseste si postgres
```yaml
  adminer:
    container_name: idp-adminer
    image: adminer
    restart: always
    ports:
      - 8080:8080
    depends_on: 
      postgres:
        condition: service_healthy
    networks:
      - adminernet
```

## Portainer
Portainer permite administrarea containerelor, acest a fost adaugat in compose
```yaml
  portainer:
      container_name: idp-portainer
      image: portainer/portainer-ce:latest
      ports:
        - 9443:9443
      volumes:
          - ./container-data/portainer:/data
          - /var/run/docker.sock:/var/run/docker.sock
      restart: unless-stopped
```
Portainer poate fi accesat la adresa [Portainer din Container](https://localhost:9443/)

## Docker Compose
Pot fi gasite 2 docker compose
```sh
./compose-swarm.yaml
./compose.yaml
```
Ambele fac in principiu acelasi lucru, doar ca ./compose-swarm.yaml folosesste imagine publicate pe docker-hub, pe cand ./compose.yaml le build-ueste pe cele locale

## Docker Swarm
Nu este implementat

## Kong
Utilizatorul trebuie sa apeleze la adresa
```sh
localhost:8000
```
Fiecare endpoint din bussines logic a fost mapat conform fisierului kong
```yml
_format_version: "2.1"

services:

# Accesarea bussiness logic login din http://localhost:8000/login
  - name: idp_bussiness_logic_login_api
    url: http://idp_bussiness_api:6002/login
    routes:
      - name: idp_bussiness_logic_api_login-route
        paths: 
          - /login

# Accesarea bussiness logic countries din http://localhost:8000/countries
  - name: idp_bussiness_logic_countries_api
    url: http://idp_bussiness_api:6002/countries
    routes:
      - name: idp_bussiness_logic_api_countries-route
        paths: 
          - /countries

# Accesarea bussiness logic city din http://localhost:8000/city
  - name: idp_bussiness_logic_city_api
    url: http://idp_bussiness_api:6002/city
    routes:
      - name: idp_bussiness_logic_api_city-route
        paths: 
          - /city

# Accesarea bussiness logic temperatures din http://localhost:8000/temperatures
  - name: idp_bussiness_logic_temperatures_api
    url: http://idp_bussiness_api:6002/temperatures
    routes:
      - name: idp_bussiness_logic_api_temperatures-route
        paths: 
          - /temperatures

# Accesarea bussiness logic city/country din http://localhost:8000/city/country
  - name: idp_bussiness_logic_city_country_api
    url: http://idp_bussiness_api:6002/city/country
    routes:
      - name: idp_bussiness_logic_api_city_country-route
        paths: 
          - /city/country

# Accesarea bussiness logic temperatures/cities din http://localhost:8000/temperatures/cities
  - name: idp_bussiness_logic_temperatures_city_api
    url: http://idp_bussiness_api:6002/temperatures/cities
    routes:
      - name: idp_bussiness_logic_api_temperatures_cities-route
        paths: 
          - /temperatures/cities

# Accesarea bussiness logic temperatures/country din http://localhost:8000/temperatures/country
  - name: idp_bussiness_logic_temperatures_country_api
    url: http://idp_bussiness_api:6002/temperatures/country
    routes:
      - name: idp_bussiness_logic_api_temperatures_country-route
        paths: 
          - /temperatures/country
```

## Monitorizare
Pentru monitorizare a fost folosit prometheus, care poate fi vazut la adresa 
[Prometheus din Container](https://localhost:9999/)
```yaml
  prometheus:
      image: prom/prometheus
      volumes:
          - ./prometheus:/etc/prometheus/
      ports:
          - 9999:9090
      networks:
          - monitoring
```
Ascolo pot fi monitorizate metricile din serviciile create de noi

## Gitlab CI/CD
Am decis de la inceput sa folosim github, asa ca am folosit github action pentru a face publice imaginele noastre la serviciile scrise de noi

### Serviciul care se ocupa de interactiunea cu DB
```yaml
name: Docker Image CI

on:
  push:
    branches: [ "main" ]
    paths:
        - 'db-microservice/**'
  pull_request:
    branches: [ "main" ]
    paths:
        - 'db-microservice/**'

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    - name: Login to Docker Hu
      uses: docker/login-action@v1
      with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_PASSWORD }}
    - name: Build and push idp-pythonapi Docker image
      uses: docker/build-push-action@v2
      with:
          context: ./db-microservice
          push: true
          tags: girnetandrei0336/idp-pythonapi:latest
```

### Serviciul de autentificare 
```yaml
name: Docker Image CI auth-microservice

on:
  push:
    branches: [ "main" ]
    paths:
        - 'auth-microservice/**'
  pull_request:
    branches: [ "main" ]
    paths:
        - 'auth-microservice/**'

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    - name: Login to Docker Hu
      uses: docker/login-action@v1
      with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_PASSWORD }}
    - name: Build and push auth-microservice Docker image
      uses: docker/build-push-action@v2
      with:
          context: ./auth-microservice
          push: true
          tags: girnetandrei0336/auth-microservice:latest
```

### Serviciul de bussiness logic
```yaml
name: Docker Image CI bussines logic

on:
  push:
    branches: [ "main" ]
    paths:
        - 'business-logic-microservice/**'
  pull_request:
    branches: [ "main" ]
    paths:
        - 'business-logic-microservice/**'

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    - name: Login to Docker Hu
      uses: docker/login-action@v1
      with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_PASSWORD }}
    - name: Build and push idp-pythonapi Docker image
      uses: docker/build-push-action@v2
      with:
          context: ./business-logic-microservice
          push: true
          tags: girnetandrei0336/idp-business-logic:latest
```
## Spre modificare
* Trebuie renuntat la build din docker compose pentru docker swarm

## PS
Andrei Girnet are configurat alt email pe git in cli, de acea apare andrei132 si Andrei Girnet :)

## Echipa Byte Crusaders
[Andrei Girnet 343C3](https://github.com/andrei132)

[Corneliu Mungiu 343C3](https://github.com/CorneliuMungiu)