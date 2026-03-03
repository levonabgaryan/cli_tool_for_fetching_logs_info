# 🚀 Log Fetcher CLI

A CLI tool designed to download and filter log errors from remote servers using SSH. It extracts microservice-specific logs and captures multi-line tracebacks.

---

## 🛠 Prerequisites

### Python 3.14
The tool requires **Python 3.14**. For Ubuntu users, install it using the deadsnakes PPA:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.14 python3.14-dev python3.14-venv python3-pip
````

## 📥 Installation
* 1 Set up Virtual Environment:
```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

* 2 Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 How to Use
Get Help
To see all available commands and options:
```bash
python main.py --help
```

* Example
```bash
python main.py fetch-log-errors-by-date-by-service-name \
  --service-name "glenn-spiro" \
  --remote-log-file-path "/path/to/remote.log" \
  --start-date-iso "2026-02-28 10:00:00" \
  --end-date-iso "2026-02-28 20:00:00" \
  --host "your.server.ip" \
  --port 22 \
  --server-user-name "admin" \
  --ssh-key-path "~/.ssh/id_rsa"
```