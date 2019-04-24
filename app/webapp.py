import json
import re
import os
import time
from flask import Flask, request
from flask import jsonify, render_template
from database.models import DataBaseEngine
from chart.chart import generate_chart


db_client = None


if os.environ["DB_TYPE"] != "sqlite3":

    db_client = DataBaseEngine(
        os.environ["DB_TYPE"], 
        db_nickname=os.environ["DB_NAME"]
    )
    
    db_client.connect()


app = Flask(__name__)


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
        sqlite3_client.execute("""{}""".format(incoming_data))

        if re.search(r'(?i)select.+', incoming_data):

            db_response, table_header = _return_query_result(sqlite3_client)

    else:

        db_client.execute("""{}""".format(incoming_data))
        
        if re.search(r'(?i)select.+', incoming_data):

            db_response, table_header = _return_query_result(db_client)

    return table_header, db_response


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
            sqlite3_client.execute("""{}""".format(incoming_data))

            if re.search(r'(?i)select.+', incoming_data):

                db_response, table_header = _return_query_result(sqlite3_client)

        else:

            db_client.execute("""{}""".format(incoming_data))
            
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


@app.route("/test_chart_js", methods=["POST", "GET"])
def generate_chart_js():

    if request.method == "POST":

        incoming_data = request.form

        _, db_response = _get_data_from_db(incoming_data["sql_query"])

        chart_data = generate_chart(
            incoming_data["chart"],
            incoming_data["title"], 
            incoming_data["dataset_label"], 
            db_response,
        )

        #print(json.dumps(chart_data, indent=4))
        return render_template(
            "webvisual.html",
            height=incoming_data["height"],
            unit=incoming_data["dataset_unit"],
            incoming_data_json=json.dumps(chart_data))

    return render_template("webdata.html")