# PostgreSQL + PostGIS in Docker

Docker compose ssetup for PgAdmin and PostgreSQL database with PostGIS plugin.

### Platform

The setup was tested on host machine OS

* Ubuntu Focal 20.04 (LTS)

### Requirements

* **[Docker >= 25.0.4](https://docs.docker.com/engine/install/ubuntu/)**

* **[Docker Compose V2](https://docs.docker.com/compose/install/linux/#install-using-the-repository)**

### Usage

create and start containers

```bash
docker compose up -d
```

you can access PgAmin on [localhost:5050](http://localhost:5050/) if you are on the same machine

or suing your host IP if you want to access it on your home network.

to find your local IP run:

```bash
hostname -I
```

one of the IPs should look like this

```bash
192.168.1.228
```

so accessing PgAdmin on your home network would be

```bash
http://192.168.1.228:5050
```

Default PgAdmin login credentials are

* E-mail: `pgadmin4@pgadmin.org`
* Password: `admin`

to stop and delete containers run

```bash
docker compose down
```

### Clean up

you can remove the Docker volumes by running

```bash
docker compose down -v
```

### Reference material

* [DockerHub: postgis/postgis](https://registry.hub.docker.com/r/postgis/postgis/)

* [GitHub: postgis/docker-postgis](https://github.com/postgis/docker-postgis)
