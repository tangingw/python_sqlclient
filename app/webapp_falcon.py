import json
import re
import os
import time
import falcon
import jinja2
#from database.models import DataBaseEngine
import datetime
import decimal
from interface.control import DBControlInterface
from app.utils import get_data_from_db


db_client = None
api_storage = None
table_key = None
previous_command = None
current_index = 0


if os.environ["DB_TYPE"] != "sqlite3":

    db_client = DBControlInterface(
        os.environ["DB_TYPE"], 
        db_nickname=os.environ["DB_NAME"]
    )
    
    db_client.connect()


def _json_serializer(obj):

    if isinstance(obj, datetime.datetime):
    
        return str(obj)
    
    elif isinstance(obj, decimal.Decimal):
    
        return str(obj)

    raise TypeError('Cannot serialize {!r} (type {})'.format(obj, type(obj)))


def _return_query_result(sql_cursor):

    return (
        sql_cursor.cursor.fetchall(), 
        [x[0] for x in sql_cursor.cursor.description]
    )


class WebDebug:

    def on_get(self, request, response):

        response.content_type = falcon.MEDIA_TEXT
        response.body = "Webapp is running"


class WebSQLAPI:

    def on_get(self, request, response):

        response.content_type = falcon.MEDIA_JSON
        
        response.media = {
            "status": falcon.HTTP_500,
            "message": "Invalid Request"
        }

    def on_post(self, request, response):

        data_from_request = request.media

        try:

            if "current_index" in data_from_request and "item_per_page" in data_from_request:

                global api_storage
                global table_key
                global previous_command

                if not api_storage or previous_command != data_from_request["sql_command"]:

                    table_key, response_db = get_data_from_db(
                        db_client, data_from_request["sql_command"]
                    )
                
                    previous_command = data_from_request["sql_command"]

                    api_storage = [
                        { table_key[i]: str(r) if (isinstance(r, datetime.datetime) or isinstance(r, decimal.Decimal)) else r  
                            for i, r in enumerate(response)}
                        for response in response_db
                    ]

                current_index = data_from_request["current_index"]
                item_per_page = data_from_request["item_per_page"]                

                response.media = {
                        "status": 200,
                        "sql_header": table_key,
                        "sql_response": api_storage[current_index: current_index + item_per_page],
                        "sql_length": len(api_storage)
                }

            else:

                table_key, response_db = get_data_from_db(db_client, data_from_request["sql_command"])

                response.media = {
                    "status": 200,
                    "sql_header": table_key,
                    "sql_response": [
                        [ 
                            str(r) if (isinstance(r, datetime.datetime) or isinstance(r, decimal.Decimal)) else r for r in response
                        ] for response in response_db
                    ]
                }

        except Exception as e:

            response.media = {
                "status": 500,
                "error_msg": str(e)
            }

class WebSQLChartjsVue:

    def on_get(self, request, response):

        response.content_type = falcon.MEDIA_JSON
        
        response.media = {
            "status": falcon.HTTP_500,
            "message": "Invalid Request"
        }

    def on_post(self, request, response):

        pass
        """incoming_data = request.media

        _, db_response = get_data_from_db(db_client, incoming_data["sql_statement"])

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
            incoming_data_json=json.dumps(chart_data)
        )
        """

class WebSQLFrontVue:

    def on_get(self, request, response):

        loader = jinja2.FileSystemLoader("app/templates")
        load_template_file = jinja2.Environment(loader=loader).get_template("webapp_vue.html")

        response.content_type = falcon.MEDIA_HTML
        response.body = load_template_file.render(db_name=os.environ["DB_NAME"])


class WebSQLStatic:

    def on_get(self, request, response, filename):

        response.status = falcon.HTTP_200
        response.content_type = 'appropriate/content-type'

        with open("app/static/{}".format(filename), 'rb') as f:
        
            response.body = f.read()


class WebSQLVisualVue:

    def on_get(self, request, response):

        loader = jinja2.FileSystemLoader("app/templates")
        load_template_file = jinja2.Environment(loader=loader).get_template("webvisual_vue.html")

        response.content_type = falcon.MEDIA_HTML
        response.body = load_template_file.render(db_name=os.environ["DB_NAME"])


app = falcon.API()
app.add_route("/debug", WebDebug())
app.add_route("/sql_api", WebSQLAPI())
app.add_route("/sql_webapp_vue", WebSQLFrontVue())
app.add_route("/static/{filename}", WebSQLStatic())
app.add_route("/sql_visual_vue", WebSQLVisualVue())