import time
import re
import os
from flask import Flask, request
from flask import jsonify, render_template
from database.models import DataBaseEngine


db_client = None


if os.environ["DB_TYPE"] != "sqlite3":

    db_client = DataBaseEngine(
        os.environ["DB_TYPE"], 
        db_nickname=os.environ["DB_NAME"]
    )
    
    db_client.connect()


app = Flask(__name__)


@app.route("/debug")
def get_debug():

    return "Webapp is running"


@app.route("/sql_webapp", methods=["POST", "GET"])
def post_command():

    def _return_query_result(sql_cursor):

        return (
            sql_cursor.cursor.fetchall(), 
            [x[0] for x in sql_cursor.cursor.description]
        )

    def _get_data_from_db(incoming_data: str) -> (list, list):

        table_header = ['']
        db_response = ['']

        if os.environ["DB_TYPE"] == "sqlite3":

            sqlite3_client = DataBaseEngine(
                "sqlite3", 
                sqlite3_filename=os.environ["DB_NAME"]
            )

            sqlite3_client.connect()
            sqlite3_client.exec("""{}""".format(incoming_data))

            if re.search(r'(?i)select.+', incoming_data):

                db_response, table_header = _return_query_result(sqlite3_client)

        else:

            db_client.exec("""{}""".format(incoming_data))
            
            if re.search(r'(?i)select.+', incoming_data):

                db_response, table_header = _return_query_result(db_client)

        return table_header, db_response


    if request.method == "POST":

        incoming_data = request.form.get("textbox")
        table_header, db_response = _get_data_from_db(incoming_data)

        return render_template(
            "response.html", 
            table_header=table_header,
            db_response=db_response
        )

    return render_template("webapp.html", db_name=os.environ["DB_NAME"])
