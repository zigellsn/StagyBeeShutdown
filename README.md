# StagyBeeShutdown

A shutdown and reboot server for StagyBee clients 

## Staring the script
*Windows*
```bash
venv\Source\activate
```
*bash*
```bash
source ./venv/bin/activate
```
Then:
```bash
python sbshutdown.py --optional_parameters_from_below...
```

## Parameter
| Parameter               | Type    |          | Meaning                                          |
|-------------------------|---------|----------|--------------------------------------------------|
| `--help` or `-h`        | toggle  | optional | Show help text                                   |
| `--version` or `-v`     | toggle  | optional | Show version                                     |
| `--port` or `-p`        | integer | optional | Port (default=8010)                              |                   
| `--token` or `-t`       | toggle  | optional | Issue token (default=False)                      |                       
| `--certificate` or `-c` | string  | optional | Server certificate file (default=certs/cert.pem) |
| `--keyfile` or `-k`     | string  | optional | Server private key file (default=certs/key.pem)  |

### Example
The call
```bash
python sbshutdown.py --port=8080 --token
```
starts a new server listening to port 8080 and issuing tokens.

### Usage
The resource `https://<ip>:<port>/token` is available via HTTP GET when starting StagyBeeShutdown in token issue mode. 
It issues a token after manually granting access on the command line. 
There can only be exactly one token for one instance of StagyBeeShutdown at all times.

To force issuing a new token delete the file `token`.

---
- **It is recommended to restrict access to the file `token/token` on file system level!**
- **It is recommended to restrict access to `certs` on file system level!**
- **Keep received tokens in a safe place all the time!**
- **It is not recommended using the parameter _--token_ permanently in production!**

---

The resources `https://<ip>:<port>/shutdown` and `https://<ip>:<port>/reboot` are always available via HTTP POST.
The payload has to be the token.
