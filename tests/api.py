import unittest
import requests
import rich
import json

API_DOMAIN = 'http://127.0.0.1:8000'

class ApiTestCase(unittest.TestCase):
    def test_get_task(self):
        response = requests.get(
            f'{API_DOMAIN}/api/task/',
            headers={
                'body':json.dumps(
                    {
                        'id':1
                    }
                )
            }
        )
        rich.print_json(response.content.decode())

    def test_get_ids(self):
        response = requests.get(
            f'{API_DOMAIN}/api/tasks/ids'
        )
        rich.print_json(response.content.decode())
    
    def test_get_tasks_by_tags(self):
        response = requests.get(
            f'{API_DOMAIN}/api/tasks/by_tags',
            headers={
                'body':json.dumps(
                    {
                        'tags':['R121ust', 'Python12']
                    }
                )
            }
        )
        rich.print_json(response.content.decode())

if __name__ == '__main__':
    unittest.main()
