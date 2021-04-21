# StagyBeeShutdown

A shutdown and reboot server for StagyBee clients 

## Usage
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
| Parameter               | Type    |          | Meaning                                       |
| ----------------------- | ------- | -------- | --------------------------------------------- |
| `--help` or `-h`        | toggle  | optional | Show help text                                |
| `--version` or `-v`     | toggle  | optional | Show version                                  |
| `--port` or `-p`        | integer | optional | Port (default=8000)                           |                   
| `--token` or `-t`       | toggle  | optional | Issue token (default=False)                   |                       
| `--certificate` or `-c` | string  | optional | Server certificate file (default=server.pem)  |

### Example
The call
```bash
python sbshutdown.py --port=8080 --token
```
starts a new server listening to port 8080 and issuing tokens.

The resource `https://<ip>:<port>/token` is now available via HTTP GET.
The resources `https://<ip>:<port>/shutdown` and `https://<ip>:<port>/reboot` are always available via HTTP POST.

**It is recommended to no use _--token_ permanently in production!**