import os
import pyodbc
import traceback
import sys

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


class IsqlApi():
    """class"""

    def __init__(self):
        """init"""
        self.port = int(os.getenv('ISQL_API_SERVER_PORT', 5050))
        self.virtuoso_dsn = str(os.getenv('ISQL_API_VIRTUOSO_DSN', "virtuoso"))
        self.virtuoso_username = str(os.getenv('ISQL_API_VIRTUOSO_USERNAME', "dba"))
        self.virtuoso_password = str(os.getenv('ISQL_API_VIRTUOSO_PASSWORD', "dba"))

        connection = pyodbc.connect("DSN={};UID={};PWD={}".format(self.virtuoso_dsn, self.virtuoso_username, self.virtuoso_password))
        connection.setencoding(encoding='utf-8')
        connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        self.cursor = connection.cursor()


@app.route("/", methods=["POST"])
def execute_isql():
    """execute isql command"""
    data = request.get_json()
    command = "{} &".format(data["command"])
    disable_log = data["disable_log"]
    sparql_select = data["sparql_select"]

    try:
        api = IsqlApi()

        formatted_rows = []
        sparql_variables = []

        if disable_log:
            api.cursor.execute("log_enable(3, 1)")

        if sparql_select:
            rows = api.cursor.execute(command).fetchall()
            if rows:
                # get SPARQL variables
                sparql_variables = [s[0] for s in rows[0].cursor_description]
                # Parse results
                for row in rows:
                    d = {}
                    for i, var in enumerate(sparql_variables):
                        if not row[i]:
                            continue
                        d[var] = row[i]
                    formatted_rows.append(d)
        else:
            api.cursor.execute(command)

        results = {"isql": True, "command": command, "vars": sparql_variables, "rows": formatted_rows, "status": 200, "message": None}

        return jsonify(results)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        results = {"isql": True, "command": command, "vars": [], "rows": [], "status": 500, "message": str(e)}
        return jsonify(results)

if __name__ == '__main__':
    api = IsqlApi()
    app.run(port=api.port)
