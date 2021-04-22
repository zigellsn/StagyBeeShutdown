# Installation

## Prerequisites

- [Python 3](https://www.python.org/)

## Installation

*Windows*

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

*bash*

```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Issue a server certificate file (default file name is `server.pem`).

## Running in Docker Container

---
**DO NOT USE SHUT DOWN SCRIPTS ON SERVERS THAT FUNCTION AS HOSTS FOR _REMOTE_ CLIENTS!**

The shut down script should run on the client side only. Otherwise, a client could shut down the Server!

Exception: Client = Server.

---

Install `inotify-tools` if necessary.

Set variable `SHUTDOWN_SIGNAL` in `scripts/shutdown_interface.sh` to the full path of the file `scripts/shutdown_signal`.

Then run

``` bash
sudo cp scripts/shutdown_interface.sh /usr/bin/
sudo cp scripts/shutdown_stagybee.service /etc/systemd/system/
sudo systemctl start shutdown_stagybee.service
sudo systemctl enable shutdown_stagybee.service
```

Issue a server certificate file (default file name is `server.pem`) and place it in the same directory as the Dockerfile.

```
mkdir token
docker build python-base/ -t stagybee/python-base:slim
docker build . -t stagybee/shutdown:slim
docker run --name my_sdserver -it -p 8010:8010 --mount type=bind,source="$(pwd)"/token,target=/home/pyuser/token --mount type=bind,source="$(pwd)"/shutdown_signal,target=/home/pyuser/shutdown_signal stagybee/shutdown:slim -t
```

Connect to the shutdown server using `https://<ip>:<port>/token`. 
Confirm the connection with 'y'. Exit the server programm with `Ctrl+C`.
Don't forget to restrict access to directory `token`!

Then run

```
docker container rm my_sdserver 
docker run --name my_sdserver -d -p 8010:8010 --restart always --mount type=bind,source="$(pwd)"/token,target=/home/pyuser/token --mount type=bind,source="$(pwd)"/shutdown_signal,target=/home/pyuser/shutdown_signal stagybee/shutdown:slim
``` 