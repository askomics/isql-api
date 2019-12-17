import pyodbc
import configparser

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


class IsqlApi():
    """class"""

    def __init__(self):
        """init"""
        conf_path = "config.ini"
        conf = configparser.ConfigParser()
        try:
            conf.read(conf_path)
        except Exception as e:
            print("Failed to read {}".format(conf_path))
            raise e

        self.port = int(conf["flask"]["port"])
        self.virtuoso_dsn = str(conf["virtuoso"]["dsn"])
        self.virtuoso_username = str(conf["virtuoso"]["username"])
        self.virtuoso_password = str(conf["virtuoso"]["password"])

        connection = pyodbc.connect("DSN={};UID={};PWD={}".format(self.virtuoso_dsn, self.virtuoso_username, self.virtuoso_password))
        self.cursor = connection.cursor()


@app.route("/", methods=["POST"])
def execute_isql():
    """execute isql command"""
    commands = request.get_json()
    results = []
    ongoing_command = ""
    try:
        api = IsqlApi()
        for command in commands:
            ongoing_command = command
            api.cursor.execute(command)
            results.append({"command": command, "status": "200", "message": None})
    except Exception as e:
        results.append({"command": ongoing_command, "status": "500", "message": str(e)})
        return jsonify(results, 500)
    return jsonify(results)

if __name__ == '__main__':
    api = IsqlApi()
    app.run(port=api.port)
