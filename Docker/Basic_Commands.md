# Basic Docker Commands
#### Docker Image
```bash
# bitnami/kafka Image von Docker Hub herunterladen und installieren
docker pull bitnami/kafka:latest

# auflisten der installierten Dockerimages
docker images

# Dockerimage löschen
docker rmi -f <Image_ID>
docker image rm <Image_Name>
```

#### docker run
```bash
docker run <parameter> image_name
    -d                      # Container läuft im Hintergrund
    --name container_name   # Bezeichner des Containers
    -p 8890:8888            # Dockerport intern 8888 gemappt auf Port 8890 extern
    run --rm                # Löschen des Containers, falls existiert
    -i                      # STDIN bleibt offen
    -v [host vz]:[container vz] #docker volume erstellen
```

#### Docker File
```bash
MAINTAINER Florian Fricke <mail@mail.com>   # Autor des Dockerfiles

FROM image_name:latest                      # Image auf dem aufgebaut wird

WORKDIR <path>

RUN sudo apt-get install -y npm
RUN ["sudo", "apt-get", "install", "-y", "npm"]

CMD echo "Hello World"                      # ähnlich wie RUN, nur 1 CMD Befehl im Dockerfile erlaubt

COPY                                        # Dateien in den Container kopieren

EXPOSE                                      # Ports festlegen
```

`docker build -t mein_image_name [path/to/dockerfile]`

#### Docker Container
```bash
# auflisten aller Container
docker ps -a

# Kommandozeile des Containers öffnen
docker exec -it <container_name> bash
docker exec -u 0 -it <container_name> bash # als root

# Kommandozeilenbefehl ausführen
docker exec -it <container_name> <befehl>
docker exec -it <container_name> pip install tensorflow

# Container stoppen
docker stop <container_id>

# Container löschen
docker rm <container_id>

# Container Logs ausgeben (werden standardmäßig angezeigt, wenn die Option -d beim run-Befehel nicht gesetzt ist)
docker logs <container_name>
docker exec -it <container_name> bash --> cd var/log && cat logfile

# IP des Container auslesen
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

# Datei aus dem Container ins lokale Verzeichnis kopieren
docker cp container_name:/foo.txt foo.txt

```

#### Docker Compose
```bash
docker-compose up
    -f <compose_filename>   # falls Datei nicht docker-compose.yml heißt
    up -d                   # Container laufen im Hintergrund
    up --build              # docker-image rebuilden

# alle Container des Compose Files stoppen
docker-compose stop

# alle Container herunterfahren und entfernen
docker-compose down
```
