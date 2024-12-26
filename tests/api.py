import unittest
import requests
import sqlite3

URL = "http://127.0.0.1:8000/"

class ApiTestCase(unittest.TestCase):
    def test_get_task(self):
        response = requests.get(f"{URL}api/get_task/?id=1")
        print(response.content)

    def test_get_ids(self):
        response = requests.get(f"{URL}api/get_tasks_ids/")
        print(response.content)

if __name__ == "__main__":
    unittest.main()
