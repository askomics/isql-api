import os
import pyodbc

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
    command = request.get_json()

    try:
        api = IsqlApi()

        rows = api.cursor.execute(command).fetchall()
        var = [s[0] for s in rows[0].cursor_description]

        # Parse results
        formatted_rows = []
        for row in rows:
            d = {}
            for i, v in enumerate(var):
                if not row[i]:
                    continue
                d[v] = row[i]
            formatted_rows.append(d)

        results = {"isql": True, "command": command, "vars": var, "rows": formatted_rows, "status": "200", "message": None}

        return jsonify(results)
    except Exception as e:
        results = {"isql": True, "command": command, "vars": [], "rows": [], "status": "500", "message": str(e)}
        return jsonify(results, 500)

if __name__ == '__main__':
    api = IsqlApi()
    app.run(port=api.port)
