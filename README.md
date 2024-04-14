# Echipa Byte Crusaders Proiect IDP

## Descriere
Scopul acestui proiect este crearea unei aplicatii bazata pe microservici care va ajuta la monitorizarea de temperaturi in diferite orase-tari.

Aplicația de Monitorizare a Temperaturilor Globale este un sistem avansat care oferă utilizatorilor o platformă interactivă pentru a accesa, actualiza și analiza datele despre temperaturile din diferite orașe și țări. Scopul principal al aplicației este de a facilita monitorizarea schimbărilor climatice și de a oferi o sursă de informații fiabilă pentru publicul larg interesat de tendințele meteorologice globale

In final va trebui sa avem o aplicatie care respecta urmatoarele conditi

- [ ] existența și integrarea celor minim 3 servicii proprii (0.9p)
    - [X] Serviciu de autentificare
    - [X] Serviciu de interactiune cu baza de date 
    - [ ] Serviciu de bussines logic
- [X] existența și integrarea unui serviciu de baze de date (0.3p)
- [X] existența și integrarea unui serviciu de utilitar DB (0.3p)
- [X] existența și integrarea Portainer sau a unui serviciu similar (0.5p)
- [ ] utilizarea Docker și rularea într-un cluster Docker Swarm (0.6p)
- [ ] existența și integrarea Kong sau a unui serviciu similar (0.6p)
- [ ] existența și integrarea unui sistem de logging sau monitorizare, cu dashboard pentru observabilitate (0.5p)
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

## Spre modificare
* La moment exista 2 retele doar, care nu sunt distribuite corect.
* Trebuie renuntat la build din docker compose pentru docker swarm

## PS
Andrei Girnet are configurat alt email pe git in cli, de acea apare andrei132 si Andrei Girnet :)

## Echipa Byte Crusaders
[Andrei Girnet 343C3](https://github.com/andrei132)

[Corneliu Mungiu 343C3](https://github.com/CorneliuMungiu)