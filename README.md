# isql API


isql-api is a HTTP server to execute virtuoso isql commands through HTTP


## Install


```bash
git clone https://github.com/xgaia/isql-api.git
cd isql-api
# create and source a python virtual environment
python3 -m venv venv && source venv/bin/activate
pip install -e .
```

## Configure

Configuration is in `config.ini`

- flask
    - port (int): flask port when running in dev mode
- virtuoso
    - dsn (str): virtuoso dsn (see firdt line of `/etc/odbc.ini`)
    - username (str): virtuoso username
    - password (str): virtuoso password


```bash
cp config.ini.template config.ini
vim config.ini
```

## Run


### Dev

```bash
python isqlapi.py
```

### Prod

```bash
gunicorn --bind localhost:5050 wsgi:app
```


## Usage

```bash
# Post a list of command to execute
curl -d '["cmd1", "cmd2"]' -H "Content-Type: application/json" -X POST http://localhost:5050
# exemple: delete a graph with transaction log mode to autocommit
curl -d '["log_enable(3,1)", "SPARQL CLEAR GRAPH <named_graph>"]' -H "Content-Type: application/json" -X POST http://localhost:5050
```
