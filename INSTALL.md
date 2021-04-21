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

Issue a server certificate file (default file name is server.pem).

## Running in Docker Container

---
**DO NOT USE SHUTDOWN SCRIPTS ON THE SAME SERVER WHEN MULTIPLE INSTANCES SIMULTANEOUSLY!**

---

Install inotify-tools if necessary.

Set variable SHUTDOWN_SIGNAL in scripts/shutdown_interface.sh to the full path of the file scripts/shutdown_signal.

Then run

``` bash
sudo cp app/scripts/shutdown_interface.sh /usr/bin/
sudo cp app/scripts/shutdown_stagybee.service /etc/systemd/system/
sudo systemctl start shutdown_stagybee.service
sudo systemctl enable shutdown_stagybee.service
```