import os
import json
import unittest
from falcon import testing
from flask import jsonify


class TestWebAppFalcon(unittest.TestCase):

    def setUp(self):

        os.environ["DB_TYPE"] = "sqlite3"
        os.environ["DB_NAME"] = "city_line"

        from app.webapp_falcon import app

        self.app = app
        self.client = testing.TestClient(self.app)

    def test_webapp_debug(self):

        result = self.client.simulate_get("/debug")        
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, "Webapp is running")
    
    def test_webapp_sql_api_get(self):

        result_get = self.client.simulate_get("/sql_api")
        self.assertEqual(result_get.status_code, 200)
        self.assertEqual(
            result_get.json["status"], "500 Internal Server Error"
        )

    def test_webapp_sql_api_post(self):

        current_item_page = 50
        result_post = self.client.simulate_post(
            "/sql_api", 
            json={
                "sql_command": "select * from cities",
                "current_index": 0,
                "item_per_page": current_item_page 
            }
        )

        self.assertEqual(result_post.status_code, 200)

        self.assertEqual(len(result_post.json["sql_response"]), current_item_page)
        self.assertSetEqual(
            set(result_post.json["sql_header"]),
            set(result_post.json["sql_response"][0].keys())
        )

    def test_webapp_sql_api_post_command(self):

        current_item_page = 7
        result_post = self.client.simulate_post(
            "/sql_api", 
            json={
                "sql_command": "table",
                "current_index": 0,
                "item_per_page": current_item_page 
            }
        )

        self.assertEqual(result_post.status_code, 200)

        self.assertEqual(len(result_post.json["sql_response"]), current_item_page)
        self.assertSetEqual(
            set(result_post.json["sql_header"]),
            set(result_post.json["sql_response"][0].keys())
        )


class TestWebAppFlask(unittest.TestCase):

    def setUp(self):

        os.environ["DB_TYPE"] = "sqlite3"
        os.environ["DB_NAME"] = "city_line"

        from app.webapp import app

        self.app = app.test_client()
        self.app.testing = True

    def test_debug(self):

        result = self.app.get("/debug")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode('utf-8'), "Webapp is running")
    
    def test_sql_api_get(self):

        result = self.app.get("/sql_api")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json["status"], 403
        )
    
    def test_sql_api_post(self):

        current_item_page = 50
        test_data = {
            "sql_command": "select * from cities",
            "current_index": 0,
            "item_per_page": current_item_page
        }

        result = self.app.post(
            "/sql_api", 
            data=json.dumps(test_data), content_type="application/json"
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            len(result.json["sql_response"]), current_item_page
        )
